import IChartProps from "../../interfaces/IChartProps";
import * as d3 from "d3";
import Line from "../figures/Line";
import RealtimeXAxis from "../axes/RealtimeXAxis";
import PriceYAxis from "../axes/PriceYAxis";
import IChart from "../../interfaces/IChart";
import {MutableRefObject} from "react";
import IAxis from "../../interfaces/IAxis";
import IFigureProps from "../../interfaces/IFigureProps";
import ISymbol from "../../../../interfaces/ISymbol";

class BasicChart implements IChart {
    readonly svg: d3.Selection<SVGElement, ISymbol[], HTMLElement, undefined>;

    private props: IChartProps;
    private svgRef: MutableRefObject<null>;
    private xAxis: IAxis;
    private yAxis: IAxis;
    private line: Line;

    constructor(props: IChartProps) {
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

        this.xAxis = new RealtimeXAxis({
            data: this.props.data,
            dimensions: this.props.dimensions
        });
        this.yAxis = new PriceYAxis({
            data: this.props.data,
            dimensions: this.props.dimensions
        });

        this.line = new Line({
            data: this.props.data,
            dimensions: this.props.dimensions,
            xScale: this.xAxis.scale,
            yScale: this.yAxis.scale
        } as IFigureProps);

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

export default BasicChart;