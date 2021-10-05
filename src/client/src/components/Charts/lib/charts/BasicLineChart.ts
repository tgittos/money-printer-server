import IChartProps from "../../interfaces/IChartProps";
import * as d3 from "d3";
import Line, {ILineProps} from "../figures/Line";
import IChart from "../../interfaces/IChart";
import {MutableRefObject} from "react";
import ILineDataPoint from "../../interfaces/ILineDataPoint";
import Grid from "../figures/Grid";
import XAxis from "../axes/XAxis";
import YAxis from "../axes/YAxis";
import moment from "moment";
import XAxisTime from "../axes/XAxisTime";

class BasicLineChart implements IChart {
    readonly svg: d3.Selection<SVGElement, ILineDataPoint[], HTMLElement, undefined>;

    private props: IChartProps<ILineDataPoint>;
    private svgRef: MutableRefObject<null>;
    private xAxis: XAxisTime;
    private yAxis: YAxis;
    private grid: Grid;
    private line: Line;

    constructor(props: IChartProps<ILineDataPoint>) {
        this.props = props;
        this.svgRef = props.svgRef;
        this.svg = d3.select(this.svgRef.current);

        this.draw();
    }

    public draw() {
        this.reset();

        this.xAxis.draw(this.svg);
        // this.yAxis.draw(this.svg);

        // this.line.draw(this.svg);
    }

    private init() {
        const { margin, width, height } = this.props.dimensions;
        const svgWidth = margin.left + margin.right + width;
        const svgHeight = margin.top + margin.bottom + height;

        const mapper = (datum: ILineDataPoint, idx: number, arr: ILineDataPoint[]) =>
            (datum as ILineDataPoint).y;

        this.xAxis = new XAxisTime({
            data: this.props.data,
            dimensions: this.props.dimensions,
            scale: d3.scaleTime,
            axis: d3.axisBottom,
            mapper: (datum: ILineDataPoint, idx: number, arr: ILineDataPoint[]) => datum.x,
            tickFormatter: (d, i) => {
                const date = moment.utc(d.valueOf());
                return date.format("f");
            }
        }) as XAxis<Date>;

        this.yAxis = new YAxis({
            data: this.props.data,
            dimensions: this.props.dimensions,
            scale: d3.scaleLinear,
            axis: d3.axisLeft,
            mapper
        });

        this.grid = new Grid({
            dimensions: this.props.dimensions,
            xDomain: this.xAxis.scale,
            yDomain: this.yAxis.scale
        })

        this.line = new Line({
            data: this.props.data,
            dimensions: this.props.dimensions,
            xScale: this.xAxis.scale,
            yScale: this.yAxis.scale
        } as ILineProps);

        this.svg
            .attr("width", svgWidth)
            .attr("height", svgHeight)
            .append("g")
            .attr("transform", "translate(" +margin.left+ "," +margin.top+ ")");
    }

    private reset() {
        this.svg.selectAll('*').remove();
        this.init();
    }
}

export default BasicLineChart;