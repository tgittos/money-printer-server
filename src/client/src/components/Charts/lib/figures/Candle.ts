import IFigureProps from "../../interfaces/IFigureProps";
import * as d3 from "d3";
import {ScaleBand} from "d3";
import ISymbol from "../../../../interfaces/ISymbol";

export interface ICandleProps extends IFigureProps {
    xBand: ScaleBand<any>;
}

class Candle {
    readonly props: ICandleProps;

    constructor(props: ICandleProps) {
        this.props = props;
    }

    public draw(svg: d3.Selection<SVGElement, ISymbol[], HTMLElement, undefined>) {
        const { data, xScale, xBand, yScale, dimensions } = this.props;
        const { margin } = dimensions;

        const mySvg = svg.append("g")
            .attr("class", "candles")
            .attr("transform", "translate(" +margin.left+ "," +margin.top+ ")");

        // draw rectangles
        const candles = mySvg.selectAll(".candle")
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
        const stems = mySvg.selectAll("g.line")
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