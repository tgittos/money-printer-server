import IFigureProps from "../../interfaces/IFigureProps";
import * as d3 from "d3";
import {ScaleBand} from "d3";

interface ICandleProps extends IFigureProps {
    xBand: ScaleBand<any>;
}

class Candle {
    private props: ICandleProps;

    constructor(props: ICandleProps) {
        this.props = props;
    }

    public draw(svg: d3.Selection<SVGElement, unknown, null, undefined>) {
        const { data, xScale, xBand, yScale } = this.props;

        console.log('data:', data);

        // draw rectangles
        const candles = svg.selectAll(".candle")
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
        const stems = svg.selectAll("g.line")
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

export default Candle;