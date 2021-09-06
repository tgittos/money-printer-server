import * as d3 from "d3";
import IFigureProps from "../../interfaces/IFigureProps";

class Line {
    private props: IFigureProps;

    constructor(props: IFigureProps) {
        this.props = props;
    }

    public draw(svg: d3.Selection<SVGElement, unknown, null, undefined>) {
        const { data, xScale, yScale } = this.props;

        const line = d3.line()
            .x(d => xScale(d.date))
            .y(d => yScale(d.close));

        svg.append("path")
            .datum(data)
            .attr("fill", "none")
            .attr("stroke", "steelblue")
            .attr("stroke-width", 1.5)
            .attr("stroke-linejoin", "round")
            .attr("stroke-linecap", "round")
            .attr("d", line);
    }
}

export default Line;
