import * as d3 from "d3";
import IFigureProps from "../../interfaces/IFigureProps";
import Symbol from "../../../../models/Symbol";
import IFigure from "../../interfaces/IFigure";

class Line implements IFigure {
    readonly props: IFigureProps;

    constructor(props: IFigureProps) {
        this.props = props;
    }

    public draw(svg: d3.Selection<SVGElement, Symbol[], HTMLElement, undefined>) {
        const { data, xScale, yScale } = this.props;

        svg.append("g").append("path")
            .datum(this.props.data)
            .attr("fill", "none")
            .attr("stroke", "steelblue")
            .attr("stroke-width", 1.5)
            .attr("d", d3.line()
                .x((d: Symbol) => {
                    return xScale(d.date)
                })
                .y((d: Symbol) => {
                    return yScale(d.latestPrice);
                }));
    }
}

export default Line;
