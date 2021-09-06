import BaseChart from "../BaseChart";
import * as d3 from "d3";
import IChartProps from "../../interfaces/IChartProps";

class LineChart extends BaseChart {

    constructor(props: IChartProps) {
        super(props);
    }

    public draw() {
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

        this._addLines(chartBody);

        svg.append("defs")
            .append("clipPath")
            .attr("id", "clip")
            .append("rect")
            .attr("width", width)
            .attr("height", height)
    }

    protected override _addAxes() {
        const { width, height, margin } = this._dimensions;
        const data = this._data;
        const dates = this._dates
        const months = this.months;

        this.xScale = d3.scaleUtc()
            .domain(d3.extent(dates))
            .range([margin.left, width - margin.right]);

        this.yScale = d3.scaleLinear()
            .domain([0, d3.max(data, d => d.close)]).nice()
            .range([height - margin.bottom, margin.top]);

        this.xAxis = d3.axisBottom()
            .scale(this.xScale)
            .tickFormat(function (d) {
                let date = new Date(d);
                let hours = date.getHours()
                let minutes = (date.getMinutes() < 10 ? '0' : '') + date.getMinutes()
                let amPM = hours < 13 ? 'am' : 'pm'
                return hours + ':' + minutes + amPM + ' ' + date.getDate() + ' ' + months[date.getMonth()] + ' ' + date.getFullYear()
            });

        this.yAxis = d3.axisLeft().scale(this.yScale);
    }

    private _addLines(svg: d3.Selection<SVGElement, unknown, null, undefined>) {
        const data = this._data;
        const xScale = this.xScale;
        const yScale = this.yScale;

        console.log('data foobar:', data);

        const line = d3.line()
            .x(d => xScale(d.date))
            .y(d => yScale(d.close));

        svg.append("path")
            .datum(data)
            .attr("fill", "none")
            .attr("stroke", "steelblue")
            .attr("stroke-width", 1.5)
            .attr("stroke-linejoin", "round")
            .attr("stroke-linecap", "round")
            .attr("d", line);
    }
}

export default LineChart;
