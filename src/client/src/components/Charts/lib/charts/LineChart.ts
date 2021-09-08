import BaseChart, {IChart} from "../BaseChart";
import * as d3 from "d3";
import IChartProps from "../../interfaces/IChartProps";
import Line from "../figures/Line";
import moment from 'moment';

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

        this.xScale = d3.scaleUtc(d3.extent(dates));
    }

    protected override _tickFormat(d: any): string {
        let date = new Date(d);
        return moment(date).format("YYYY:MM:dd hh:MM:SS");
    }
}

export default LineChart;
