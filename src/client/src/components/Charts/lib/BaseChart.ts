import IChartProps from "../interfaces/IChartProps";
import {MutableRefObject} from "react";
import IChartDimensions from "../interfaces/IChartDimensions";
import * as d3 from "d3";
import {Axis, AxisDomain, ScaleLinear} from "d3";
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
    protected yScale: any;

    protected constructor(props: IChartProps) {
        console.log('props:', props);
        this._props = props;
        this._data = props.data;
        this._dates = [];
        this._dimensions = props.dimensions;

        this.xScale = null;
        this.xAxis = null;
        this.yScale = null;
        this.yAxis = null;

        this._svgRef = props.svgRef;
        this._svg = d3.select(this._svgRef.current);

        this.draw();
    }

    public draw() {
        this._createScales();
        this._createAxes();

        this._resetSvg();
        this._renderAxes()
        this._renderFigures();
    }

    protected _resetSvg(): void {
        const { margin, width, height } = this._dimensions;
        const svgWidth = margin.left + margin.right + width;
        const svgHeight = margin.top + margin.bottom + height;

        this._svg.remove();
        this._svg
            .attr("width", svgWidth)
            .attr("height", svgHeight)
            .append("g")
            .attr("transform", "translate(" +margin.left+ "," +margin.top+ ")");
    }

    protected abstract _createScales(): void

    protected abstract _xTickFormatter(d: AxisDomain, i: Number): string;

    protected _createAxes() {
        const tf = this._xTickFormatter;

        console.log('this.xScale:', this.xScale);

        this.xAxis = d3.axisBottom(this.xScale);
            //.tickFormat(tf);

        this.yAxis = d3.axisLeft(this.yScale);
    };

    protected _renderAxes() {
        const { height } = this._dimensions;
        const xAxis = this.xAxis;
        const yAxis = this.yAxis;

        console.log('xAxis:', xAxis);

        this._svg.append("g")
            .attr("class", "axis x-axis") //Assign "axis" class
            .attr("transform", "translate(0," + height + ")")
            .call(xAxis)

        this._svg.append("g")
            .attr("class", "axis y-axis")
            .call(yAxis);
    }

    protected abstract _renderFigures(): void;
}

export default BaseChart;