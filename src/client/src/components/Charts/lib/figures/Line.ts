import * as d3 from "d3";
import IFigureProps from "../../interfaces/IFigureProps";
import Symbol from "../../../../models/Symbol";

class Line {
    readonly props: IFigureProps;

    constructor(props: IFigureProps) {
        this.props = props;
    }

    public draw(svg: d3.Selection<SVGElement, Symbol[], HTMLElement, undefined>) {
        const { data, xScale, yScale } = this.props;

        const g = svg.append("g");

        g.append("path")
            .datum(data)
            .attr("fill", "none")
            .attr("stroke", "steelblue")
            .attr("stroke-width", 1.5)
            // .attr("stroke-linejoin", "round")
            // .attr("stroke-linecap", "round")
            .attr("d", d3.line()
                .x((d: Symbol) => xScale(d.date))
                .y((d: Symbol) => yScale(d.latestPrice)));
    }
}

export default Line;
