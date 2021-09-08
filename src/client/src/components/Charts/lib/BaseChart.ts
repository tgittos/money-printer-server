import IChartProps from "../interfaces/IChartProps";
import {MutableRefObject} from "react";
import IChartDimensions from "../interfaces/IChartDimensions";
import * as d3 from "d3";
import {Axis, ScaleLinear} from "d3";
import Symbol from '../../../models/Symbol';
import moment from 'moment';

type NullableDate = Date | null;

export interface IChartFactory {
    new(props: IChartProps): IChart;
}

export interface IChart {
}

export const createChart = (chartFactory: IChartFactory, props: IChartProps): IChart => {
    return new chartFactory(props);
}

export abstract class BaseChart {
    protected _props: IChartProps;
    protected _data: Symbol[];
    protected _dates: NullableDate[];
    protected _dimensions: IChartDimensions;
    protected _svgRef: MutableRefObject<null>;
    protected _svg: d3.Selection<SVGGElement, unknown, HTMLElement, any> | null;
    protected xScale: any;
    protected xAxis: Axis<any> | null;
    protected yAxis: Axis<any> | null;
    protected yScale: ScaleLinear<number, number> | null;

    protected constructor(props: IChartProps) {
        this._props = props;
        this._data = props.data;
        this._dates = [];
        this._dimensions = props.dimensions;
        this._svgRef = props.svgRef;
        this._svg = null;
        this.xScale = null;
        this.xAxis = null;
        this.yScale = null;
        this.yAxis = null;

        this._fixData();
        this.draw();
    }

    public draw() {
        const dimensions = this._dimensions;
        const { margin } = this._dimensions;
        const svgWidth = dimensions.margin.left + dimensions.margin.right + dimensions.width;
        const svgHeight = dimensions.margin.top + dimensions.margin.bottom + dimensions.height;

        this._svg = d3.select(this._svgRef.current)
            .attr("width", svgWidth)
            .attr("height", svgHeight)
            .append("g")
            .attr("transform", "translate(" +margin.left+ "," +margin.top+ ")");

        this._createScales();
        this._addAxes();
        this._renderAxes()

        this._renderFigures();
    }

    protected abstract _renderFigures(): void;

    private _fixData() {
        const dateFormat = d3.timeParse("%Y-%m-%d");
        for (let i = 0; i < this._data.length; i++) {
            // this._data[i].date = dateFormat(this._data[i].date?.toString() ?? '')
        }
        this._dates = this._data.map(d => d.date);
    }

    protected _createScales() {
        const { width, height, margin } = this._dimensions;
        const data = this._data;
        const dates = this._dates;

        this.xScale = d3.scaleLinear().domain([-1, dates.length])
            .range([0, width])

        const yMin = d3.min(data.map(r => r.low));
        const yMax = d3.max(data.map(r => r.high));

        this.yScale = d3.scaleLinear().domain([yMin as number, yMax as number]).range([height, 0]).nice()
            .range([height - margin.bottom, margin.top]);
    }

    protected _tickFormat(d: any) {
        const dates = this._dates;

        console.log('dates:', dates);
        console.log('d:', d);
        let date = dates[d];
        console.log('date:', date);

        if (date == null) {
            return 'fucked';
        }

        return moment(date).format("YYYY:MM:dd hh:MM:SS");
    }

    protected _addAxes() {
        const { width, height } = this._dimensions;
        const dates = this._dates;
        const xScale = this.xScale;
        const yScale = this.yScale;
        const tf = this._tickFormat.bind(this);

        this.xAxis = d3.axisBottom(xScale)
            .tickFormat(tf);

        this.yAxis = d3.axisLeft(yScale);
    };

    protected _renderAxes() {
        const { height } = this._dimensions;
        const xAxis = this.xAxis;
        const yAxis = this.yAxis;

        const svg = this._svg;

        const gX = svg.append("g")
            .attr("class", "axis x-axis") //Assign "axis" class
            .attr("transform", "translate(0," + height + ")")
            .call(xAxis)

        const gY = svg.append("g")
            .attr("class", "axis y-axis")
            .call(yAxis);
    }
}

export default BaseChart;