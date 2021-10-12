import IFigureProps from "../../interfaces/IFigureProps";
import * as d3 from "d3";
import {ScaleBand} from "d3";
import ICandleDataPoint from "../../interfaces/ICandleDataPoint";

export interface ICandleProps extends IFigureProps {
    data: ICandleDataPoint[];
}

class Candle {
    readonly props: ICandleProps;

    constructor(props: ICandleProps) {
        this.props = props;
    }

    public draw(svg: d3.Selection<SVGElement, ICandleDataPoint[], HTMLElement, undefined>) {
        const { data, xScale, yScale, dimensions: { margin, width } } = this.props;

        const dates = this.props.data.map((datum: ICandleDataPoint) => datum.date);
        const xBand = d3.scaleBand<number>(d3.range(dates.length), [0, width])
            .padding(0.3);

        const mySvg = svg.append("g")
            .attr("class", "candles")
            .attr("transform", "translate(" +margin.left+ "," +margin.top+ ")");

        // draw rectangles
        const candles = mySvg.selectAll(".candle")
            .data(data)
            .enter()
            .append("rect")
            .attr('x', (d, i) => xBand(i) - xBand.bandwidth())
            .attr("class", "candle")
            .attr('y', d => yScale(Math.max(d?.open, d?.close)))
            .attr('width', xBand.bandwidth())
            .attr('height', d => (d?.open === d?.close) ? 1 : yScale(Math.min(d?.open, d?.close))-yScale(Math.max(d?.open, d?.close)))
            .attr("fill", d => (d?.open === d?.close) ? "silver" : (d?.open > d?.close) ? "red" : "green")

        // draw high and low
        const stems = mySvg.selectAll(".candle-stem")
            .data(data)
            .enter()
            .append("line")
            .attr("class", "stem")
            .attr("x1", (d, i) => xBand(i) - xBand.bandwidth()/2)
            .attr("x2", (d, i) => xBand(i) - xBand.bandwidth()/2)
            .attr("y1", d => yScale(d?.high))
            .attr("y2", d => yScale(d?.low))
            .attr("stroke", d => (d?.open === d?.close) ? "white" : (d?.open > d?.close) ? "red" : "green");
    }
}

export default Candle;