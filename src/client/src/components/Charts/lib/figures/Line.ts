import * as d3 from "d3";
import IFigureProps from "../../interfaces/IFigureProps";
import ISymbol, {SortDescending} from "../../../../interfaces/ISymbol";

class Line {
    readonly props: IFigureProps;

    constructor(props: IFigureProps) {
        this.props = props;
    }

    public draw(svg: d3.Selection<SVGElement, ISymbol[], HTMLElement, undefined>) {
        const { xScale, yScale, dimensions } = this.props;
        const { margin } = dimensions;

        const lineGenerator = d3.line<ISymbol>()
            .defined((d: ISymbol) => {
                return !!d.close;
            })
            .x((d: ISymbol) => {
                const val = xScale(d.date);
                return val;
            })
            .y((d: ISymbol) => {
                const val = yScale(d.close);
                return val;
            });

        svg.append("g")
                .attr("transform", "translate(" +margin.left+ "," +margin.top+ ")")
            .append("path")
            .datum(this.props.data)
            .attr("fill", "none")
            .attr("stroke", "steelblue")
            .attr("stroke-width", 1.5)
            .attr("d", lineGenerator);
    }
}

export default Line;
