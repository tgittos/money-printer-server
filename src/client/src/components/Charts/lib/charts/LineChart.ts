import BaseChart, {IChart} from "../BaseChart";
import * as d3 from "d3";
import IChartProps from "../../interfaces/IChartProps";
import Line from "../figures/Line";

class LineChart extends BaseChart implements IChart {

    constructor(props: IChartProps) {
        super(props);
    }

    protected override _renderFigures() {
        const svg = this._svg;

        const lines = new Line({
            data: this._data,
            xScale: this.xScale,
            yScale: this.yScale
        });
        lines.draw(svg);
    }

    protected override _createScales() {
        super._createScales();

        const { width, height, margin } = this._dimensions;
        const dates = this._dates;

        this.xScale = d3.scaleUtc()
            .domain(d3.extent(dates))
            .range([margin.left, width - margin.right]);
    }

    protected override _tickFormat(d): string {
        const months = this.months;

        let date = new Date(d);
        let hours = date.getHours()
        let minutes = (date.getMinutes() < 10 ? '0' : '') + date.getMinutes()
        let amPM = hours < 13 ? 'am' : 'pm'
        return hours + ':' + minutes + amPM + ' ' + date.getDate() + ' ' + months[date.getMonth()] + ' ' + date.getFullYear()
    }
}

export default LineChart;
