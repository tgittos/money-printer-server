import * as d3 from "d3";
import IFigureProps from "../../interfaces/IFigureProps";
import Symbol from "../../../../models/Symbol";
import IFigure from "../../interfaces/IFigure";

class Line {
    readonly props: IFigureProps;

    constructor(props: IFigureProps) {
        this.props = props;
    }

    public draw(svg: d3.Selection<SVGElement, Symbol[], HTMLElement, undefined>) {
        const { data, xScale, yScale } = this.props;

        const lineGenerator = d3.line<Symbol>()
            .x((d: Symbol) => {
                return xScale(d.date) as number;
            })
            .y((d: Symbol) => {
                return yScale(d.latestPrice) as number;
            });

        svg.append("g").append("path")
            .datum(this.props.data)
            .attr("fill", "none")
            .attr("stroke", "steelblue")
            .attr("stroke-width", 1.5)
            .attr("d", lineGenerator);
    }
}

export default Line;
