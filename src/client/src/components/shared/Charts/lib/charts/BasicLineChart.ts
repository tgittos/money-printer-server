import IChartProps from "../../interfaces/IChartProps";
import * as d3 from "d3";
import Line, {ILineProps} from "../figures/Line";
import IChart from "../../interfaces/IChart";
import {MutableRefObject} from "react";
import ILineDataPoint from "../../interfaces/ILineDataPoint";
import Grid from "../figures/Grid";
import XAxis, {IXAxisProps} from "../axes/XAxis";
import YAxis, {IYAxisProps} from "../axes/YAxis";
import moment from "moment";
import {formatAsCurrency} from "../../../../../lib/Utilities";

class BasicLineChart implements IChart {
    readonly svg: d3.Selection<SVGElement, ILineDataPoint[], HTMLElement, undefined>;

    private props: IChartProps<ILineDataPoint>;
    private svgRef: MutableRefObject<null>;
    private xScale: d3.ScaleTime<number, Date>;
    private yScale: d3.ScaleLinear<number, number>;
    private xAxis: XAxis<Date>;
    private yAxis: YAxis;
    private grid: Grid;
    private line: Line;

    constructor(props: IChartProps<ILineDataPoint>) {
        this.props = props;
        this.svgRef = props.svgRef;
        this.svg = d3.select(this.svgRef.current);

        // as soon as we're built, trigger a draw call
        this.draw();
    }

    public draw() {
        // reset the svg that we were passed in
        this.reset();

        // draw the axis
        this.xAxis.draw(this.svg);
        this.yAxis.draw(this.svg);

        // draw the grid
        this.grid.draw(this.svg);

        // draw the data line
        this.line.draw(this.svg);
    }

    private init() {

        const { margin, width, height } = this.props.dimensions;
        const svgWidth = margin.left + margin.right + width;
        const svgHeight = margin.top + margin.bottom + height;

        const dateDomain = this.props.data.map((datum: ILineDataPoint) => datum.x);
        const valDomain = this.props.data.map(datum => datum.y);

        // build scales from data and chart dimensions
        this.xScale = d3.scaleTime(d3.extent(dateDomain), [0, width]);
        this.yScale = d3.scaleLinear(d3.extent(valDomain), [height, 0]);

        // build a date based XAxis, and format each date for the x axis
        this.xAxis = new XAxis<Date>({
            data: this.props.data,
            dimensions: this.props.dimensions,
            scale: this.xScale,
            axis: d3.axisBottom,
            // tickCount: d3.utcDay.every(5)
            mapper: (datum: ILineDataPoint, idx: number, arr: ILineDataPoint[]) => datum.x,
            tickFormatter: (d: Date, i: number): string => {
                const date = moment.utc(d.valueOf());
                return date.format();
            }
        } as unknown as IXAxisProps<Date>);

        // build a basic YAxis, and format each number as a currency number
        this.yAxis = new YAxis({
            data: this.props.data,
            dimensions: this.props.dimensions,
            scale: this.yScale,
            axis: d3.axisLeft,
            mapper: (datum: ILineDataPoint, idx: number, arr: ILineDataPoint[]) =>
                (datum as ILineDataPoint).y,
        } as IYAxisProps);

        // add a grid at each tick on each axis
        this.grid = new Grid({
            dimensions: this.props.dimensions,
            xDomain: this.xScale,
            yDomain: this.yScale
        });

        // add a line figure for the data in the chart
        this.line = new Line({
            data: this.props.data,
            dimensions: this.props.dimensions,
            xScale: this.xScale,
            yScale: this.yScale
        } as ILineProps);

        // initialize the actual SVG ready for rendering
        this.svg
            .attr("width", svgWidth)
            .attr("height", svgHeight)
            .append("g")
            .attr("transform", "translate(" +margin.left+ "," +margin.top+ ")");

    }

    private reset() {
        // clear the chart and build everything from scratch
        this.svg.selectAll('*').remove();
        this.init();
    }

}

export default BasicLineChart;