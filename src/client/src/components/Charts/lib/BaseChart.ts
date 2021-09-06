import IChartProps from "../interfaces/IChartProps";
import {ISymbol} from "../../../models/Symbol";
import {MutableRefObject} from "react";
import IChartDimensions from "../interfaces/IChartDimensions";
import * as d3 from "d3";
import {Axis, ScaleBand, ScaleLinear} from "d3";

type NullableDate = Date | null;

export default abstract class BaseChart {
    protected _data: ISymbol[];
    protected _dates: NullableDate[];
    protected _dimensions: IChartDimensions;
    protected _svgRef: MutableRefObject<null>;
    protected xScale: ScaleLinear<number, number>;
    protected xAxis: Axis<any>;
    protected yAxis: Axis<any>;
    protected yScale: ScaleLinear<number, number>;

    // TODO - rename this, or change it to a mapped fn or something
    protected months = {
        0 : 'Jan',
        1 : 'Feb',
        2 : 'Mar',
        3 : 'Apr',
        4 : 'May',
        5 : 'Jun',
        6 : 'Jul',
        7 : 'Aug',
        8 : 'Sep',
        9 : 'Oct',
        10 : 'Nov',
        11 : 'Dec'
    };

    protected constructor(props: IChartProps) {
        this._data = props.data;
        this._dimensions = props.dimensions;
        this._svgRef = props.svgRef;

        this._fixData();
        this.draw();
    }

    abstract draw();

    private _fixData() {
        const dateFormat = d3.timeParse("%Y-%m-%d");
        for (let i = 0; i < this._data.length; i++) {
            this._data[i].date = dateFormat(this._data[i].date?.toString() ?? '')
        }
        this._dates = this._data.map(d => d.date);
    }

    protected _createScales() {
        const { width, height } = this._dimensions;
        const data = this._data;
        const dates = this._dates;

        this.xScale = d3.scaleLinear().domain([-1, dates.length])
            .range([0, width])

        const yMin = d3.min(data.map(r => r.low));
        const yMax = d3.max(data.map(r => r.high));

        this.yScale = d3.scaleLinear().domain([yMin, yMax]).range([height, 0]).nice();
    }

    protected _addAxes() {
        const { width, height } = this._dimensions;
        const dates = this._dates;
        const months = this.months;
        const xScale = this.xScale;
        const yScale = this.yScale;

        this.xAxis = d3.axisBottom()
            .scale(xScale)
            .tickFormat(function (d) {
                let date = dates[d];
                let hours = date.getHours()
                let minutes = (date.getMinutes() < 10 ? '0' : '') + date.getMinutes()
                let amPM = hours < 13 ? 'am' : 'pm'
                return hours + ':' + minutes + amPM + ' ' + date.getDate() + ' ' + months[date.getMonth()] + ' ' + date.getFullYear()
            });

        this.yAxis = d3.axisLeft().scale(yScale);
    };

    protected _renderAxes(svg: d3.Selection<SVGGElement, unknown, null, undefined>) {
        const { height } = this._dimensions;
        const xAxis = this.xAxis;
        const yAxis = this.yAxis;

        const gX = svg.append("g")
            .attr("class", "axis x-axis") //Assign "axis" class
            .attr("transform", "translate(0," + height + ")")
            .call(xAxis)

        const gY = svg.append("g")
            .attr("class", "axis y-axis")
            .call(yAxis);
    }


    protected _wrap(text: string[], width: number) {
        text.each(function() {
            const text = d3.select(this),
                words = text.text().split(/\s+/).reverse(),
                lineHeight = 1.1, // ems
                y = text.attr("y"),
                dy = parseFloat(text.attr("dy"));
            let line = [],
                word,
                lineNumber = 0,
                tspan = text.text(null).append("tspan").attr("x", 0).attr("y", y).attr("dy", dy + "em");
            while (word = words.pop()) {
                line.push(word);
                tspan.text(line.join(" "));
                if (tspan.node().getComputedTextLength() ?? 0 > width) {
                    line.pop();
                    tspan.text(line.join(" "));
                    line = [word];
                    tspan = text.append("tspan").attr("x", 0).attr("y", y).attr("dy", ++lineNumber * lineHeight + dy + "em").text(word);
                }
            }
        });
    }
}