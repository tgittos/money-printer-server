import IChartProps from "../../interfaces/IChartProps";
import * as d3 from "d3";
import Symbol from "../../../../models/Symbol";
import moment from 'moment';


const BasicChart = function(props: IChartProps) {
    (this as BasicChart).props = props;
    this.svgRef = props.svgRef;
    this.svg = d3.select(this.svgRef.current);

    this._init();
    this.draw();
}

BasicChart.prototype._init = function() {
    const { margin, width, height } = this.props.dimensions;
    const svgWidth = margin.left + margin.right + width;
    const svgHeight = margin.top + margin.bottom + height;

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

BasicChart.prototype._createScales = function() {
    const { width, height, margin } = this.props.dimensions;
    const svgWidth = margin.left + margin.right + width;
    const svgHeight = margin.top + margin.bottom + height;

    const now = new Date();
    now.setMinutes(now.getMinutes() + 15);
    const windowStart = moment(now).subtract(1, 'hour');

    this.xScale = d3.scaleTime()
        .domain([windowStart, now])
        .range([0, width]);

    const yMin = d3.min(this.props.data, (s: Symbol) => +s.week52Low);
    const yMax = d3.max(this.props.data, (s: Symbol) => +s.week52High);

    this.yScale = d3.scaleLinear()
        .domain([yMin, yMax + yMax * 0.1])
        .range([height, 0]);
}

BasicChart.prototype._createAxes = function () {
    this.xAxis = d3.axisBottom(this.xScale)
        .ticks(d3.timeMinute.every(2))
        .tickFormat(d3.timeFormat('%H:%M'));
    this.yAxis = d3.axisLeft(this.yScale);
}

BasicChart.prototype.draw = function() {
    this._reset();

    this._createScales();
    this._createAxes();

    this._drawAxes();
    this._drawFigures();
}

BasicChart.prototype._drawAxes = function() {
    const { height, margin } = this.props.dimensions;
    const xAxis = this.xAxis;
    const yAxis = this.yAxis;

    this.svg.append("g")
        .attr("class", "axis x-axis") //Assign "axis" class
        .attr("transform", "translate(" + margin.left + "," + height + ")")
        .call(xAxis)

    this.svg.append("g")
        .attr("class", "axis y-axis")
        .attr("transform", "translate(" + margin.left + ", 0)")
        .call(yAxis);
}

BasicChart.prototype._drawFigures = function() {
    const x = this.xScale;
    const y = this.yScale;

    this.svg.append("g").append("path")
        .datum(this.props.data)
        .attr("fill", "none")
        .attr("stroke", "steelblue")
        .attr("stroke-width", 1.5)
        .attr("d", d3.line()
            .x((d: Symbol) => {
                return x(d.date)
            })
            .y((d: Symbol) => {
                return y(d.latestPrice);
            }));
}

export default BasicChart;