import BaseChart, {IChart} from "../BaseChart";
import * as d3 from "d3";
import IChartProps from "../../interfaces/IChartProps";
import Line from "../figures/Line";
import moment from 'moment';
import Symbol from '../../../../models/Symbol'
import {AxisDomain} from "d3";
import IFigureProps from "../../interfaces/IFigureProps";

class LineChart extends BaseChart implements IChart {

    constructor(props: IChartProps) {
        super(props);
    }

    protected override _createScales() {
        this.xScale = d3.scaleUtc(d3.extent(this._data,
            (s: Symbol) => s.date));
    }

    protected override _xTickFormatter(d: AxisDomain, i: Number): string {
        const date = this.xScale(d);
        return moment(date).format("YYYY:MM:dd hh:MM:SS");
    }

    protected override _renderFigures() {
        const lines = new Line({
            data: this._data,
            xScale: this.xScale,
            yScale: this.yScale
        } as IFigureProps);

        lines.draw(this._svg);
    }

}

export default LineChart;
