import IChartProps from "../../interfaces/IChartProps";
import * as d3 from "d3";
import Line from "../figures/Line";
import RealtimeXAxis from "../axes/RealtimeXAxis";
import PriceYAxis from "../axes/PriceYAxis";
import Candle from "../figures/Candle";
import CandleXAxis from "../axes/CandleXAxis";
import IChart from "../../interfaces/IChart";

const BasicCandleChart = function(props: IChartProps) {
    this.props = props;
    this.svgRef = props.svgRef;
    this.svg = d3.select(this.svgRef.current);

    this.draw();
} as IChart

BasicCandleChart.prototype.draw = function() {
    this._reset();

    this.xAxis.draw(this.svg);
    this.yAxis.draw(this.svg);

    this.candles.draw(this.svg);
}

BasicCandleChart.prototype._init = function() {
    const { margin, width, height } = this.props.dimensions;
    const svgWidth = margin.left + margin.right + width;
    const svgHeight = margin.top + margin.bottom + height;

    this.props.data = this.props.data.reverse();

    this.xAxis = new CandleXAxis({
        data: this.props.data,
        dimensions: this.props.dimensions
    });
    this.yAxis = new PriceYAxis({
        data: this.props.data,
        dimensions: this.props.dimensions
    });

    this.xBand = d3.scaleBand()
        .domain(d3.range(-1, this.props.data.length))
        .range([0, width])
        .padding(0.3)

    this.candles = new Candle({
        data: this.props.data,
        xScale: this.xAxis.scale,
        yScale: this.yAxis.scale,
        xBand: this.xBand,
        dimensions: this.props.dimensions
    });

    this.svg
        .attr("width", svgWidth)
        .attr("height", svgHeight)
        .append("g")
        .attr("transform", "translate(" +margin.left+ "," +margin.top+ ")");
}

BasicCandleChart.prototype._reset = function() {
    this.svg.selectAll('*').remove();
    this._init();
}

export default BasicCandleChart;