import IChartProps from "../../interfaces/IChartProps";
import * as d3 from "d3";
import Line from "../figures/Line";
import RealtimeXAxis from "../axes/RealtimeXAxis";
import PriceYAxis from "../axes/PriceYAxis";


const BasicChart = function(props: IChartProps) {
    (this as any).props = props;
    this.svgRef = props.svgRef;
    this.svg = d3.select(this.svgRef.current);

    this.draw();
}

BasicChart.prototype.draw = function() {
    this._reset();

    this.xAxis.draw(this.svg);
    this.yAxis.draw(this.svg);
    this.line.draw(this.svg);
}

BasicChart.prototype._init = function() {
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
        xScale: this.xAxis.scale,
        yScale: this.yAxis.scale
    });

    this.svg
        .attr("width", svgWidth)
        .attr("height", svgHeight)
        .append("g")
        .attr("transform", "translate(" +margin.left+ "," +margin.top+ ")");
}

BasicChart.prototype._reset = function() {
    this.svg.selectAll('*').remove();
    this._init();
}

export default BasicChart;