import BaseChart from "../BaseChart";
import {ScaleBand, ScaleLinear} from "d3";
import IChartProps from "../../interfaces/IChartProps";
import * as d3 from "d3";


class CandleChart extends BaseChart {

    protected xBand: ScaleBand<any>;

    constructor(props: IChartProps) {
        super(props);

    }

    public draw() {
        const data = this._data;
        const dimensions = this._dimensions;
        const { width, height, margin } = this._dimensions;
        const svgWidth = dimensions.margin.left + dimensions.margin.right + dimensions.width;
        const svgHeight = dimensions.margin.top + dimensions.margin.bottom + dimensions.height;

        const svg = d3.select(this._svgRef.current)
            .attr("width", svgWidth)
            .attr("height", svgHeight)
            .append("g")
            .attr("transform", "translate(" +margin.left+ "," +margin.top+ ")");

        svg.append("rect")
            .attr("id","rect")
            .attr("width", width)
            .attr("height", height)
            .style("fill", "none")
            .style("pointer-events", "all")
            .attr("clip-path", "url(#clip)")

        this._createScales();
        this._addAxes();
        this._renderAxes(svg)

        const chartBody = svg.append("g")
            .attr("class", "chartBody")
            .attr("clip-path", "url(#clip)");

        this._addCandles(chartBody);

        svg.append("defs")
            .append("clipPath")
            .attr("id", "clip")
            .append("rect")
            .attr("width", width)
            .attr("height", height)
    };

    protected override _addAxes() {
        super._addAxes();

        const dates = this._dates;
        const { width } = this._dimensions;

        this.xBand = d3.scaleBand().domain(
            d3.range(-1, dates.length)
                .map(r => r.toString())
        ).range([0, width]).padding(0.3);
    }

    protected override _renderAxes(svg: d3.Selection<SVGGElement, unknown, null, undefined>) {
        const { height } = this._dimensions;
        const xAxis = this.xAxis;
        const xBand = this.xBand;
        const yAxis = this.yAxis;
        const wrap = this._wrap;

        const gX = svg.append("g")
            .attr("class", "axis x-axis") //Assign "axis" class
            .attr("transform", "translate(0," + height + ")")
            .call(xAxis)

        gX.selectAll(".tick text")
            .call(wrap, xBand.bandwidth())

        const gY = svg.append("g")
            .attr("class", "axis y-axis")
            .call(yAxis);
    }

    private _addCandles(chartBody: d3.Selection<SVGGElement, unknown, null, undefined>) {
        const data = this._data;
        const xScale = this.xScale;
        const xBand = this.xBand;
        const yScale = this.yScale;

        // draw rectangles
        const candles = chartBody.selectAll(".candle")
            .data(data)
            .enter()
            .append("rect")
            .attr('x', (d, i) => xScale(i) - xBand.bandwidth())
            .attr("class", "candle")
            .attr('y', d => yScale(Math.max(d.open, d.close)))
            .attr('width', xBand.bandwidth())
            .attr('height', d => (d.open === d.close) ? 1 : yScale(Math.min(d.open, d.close))-yScale(Math.max(d.open, d.close)))
            .attr("fill", d => (d.open === d.close) ? "silver" : (d.open > d.close) ? "red" : "green")

        // draw high and low
        const stems = chartBody.selectAll("g.line")
            .data(data)
            .enter()
            .append("line")
            .attr("class", "stem")
            .attr("x1", (d, i) => xScale(i) - xBand.bandwidth()/2)
            .attr("x2", (d, i) => xScale(i) - xBand.bandwidth()/2)
            .attr("y1", d => yScale(d.high))
            .attr("y2", d => yScale(d.low))
            .attr("stroke", d => (d.open === d.close) ? "white" : (d.open > d.close) ? "red" : "green");
    }
}

export default CandleChart;
