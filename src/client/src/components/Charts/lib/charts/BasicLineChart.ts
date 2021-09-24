import IChartProps from "../../interfaces/IChartProps";
import * as d3 from "d3";
import Line, {ILineProps} from "../figures/Line";
import SimpleYAxis from "../axes/SimpleYAxis";
import IChart from "../../interfaces/IChart";
import {MutableRefObject} from "react";
import ILineDataPoint from "../../interfaces/ILineDataPoint";
import SimpleXAxis from "../axes/SimpleXAxis";

class BasicLineChart implements IChart {
    readonly svg: d3.Selection<SVGElement, ILineDataPoint[], HTMLElement, undefined>;

    private props: IChartProps<ILineDataPoint>;
    private svgRef: MutableRefObject<null>;
    private xAxis: SimpleXAxis;
    private yAxis: SimpleYAxis;
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
        this.yAxis.draw(this.svg);

        this.line.draw(this.svg);
    }

    private init() {
        const { margin, width, height } = this.props.dimensions;
        const svgWidth = margin.left + margin.right + width;
        const svgHeight = margin.top + margin.bottom + height;

        this.xAxis = new SimpleXAxis({
            data: this.props.data,
            dimensions: this.props.dimensions,
            mapper: (data: ILineDataPoint) => data?.x
        });
        this.yAxis = new SimpleYAxis({
            data: this.props.data,
            dimensions: this.props.dimensions,
            mapper: (data: ILineDataPoint) => data?.y
        });

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