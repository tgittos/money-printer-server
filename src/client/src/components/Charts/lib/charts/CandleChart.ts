import BaseChart, {IChart} from "../BaseChart";
import {ScaleBand, ScaleLinear} from "d3";
import IChartProps from "../../interfaces/IChartProps";
import * as d3 from "d3";
import Candle from "../figures/Candle";


class CandleChart extends BaseChart implements IChart {

    protected xBand: ScaleBand<any>;

    constructor(props: IChartProps) {
        super(props);

    }

    protected override _renderFigures() {
        const data = this._data;
        const dimensions = this._dimensions;
        const { width, height, margin } = this._dimensions;

        const svg = this._svg;

        svg.append("rect")
            .attr("id","rect")
            .attr("width", width)
            .attr("height", height)
            .style("fill", "none")
            .style("pointer-events", "all")
            .attr("clip-path", "url(#clip)")

        const candles = new Candle({
            data: data,
            xScale: this.xScale,
            xBand: this.xBand,
            yScale: this.yScale,
        });
        candles.draw(svg);
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
}

export default CandleChart;
