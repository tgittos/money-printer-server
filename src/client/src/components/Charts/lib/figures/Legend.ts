import * as d3 from "d3";
import IFigureDataPoint from "../../interfaces/IFigureDataPoint";
import {ScaleOrdinal, style} from "d3";

export interface ILegendProps {
    x: number,
    y: number,
    size: number;
    labels: string[]
    domain: ScaleOrdinal<any, any>
}

class Legend {
    readonly props: ILegendProps;

    constructor(props: ILegendProps) {
        this.props = props;
    }

    public draw(svg: d3.Selection<SVGElement, IFigureDataPoint[], HTMLElement, undefined>) {
        const { labels, domain, } = this.props
        const data = [].concat(labels) as string[]

        const size = this.props.size ?? 10;
        const x = this.props.x ?? 10;
        const y = this.props.y ?? 10;

        const mySvg = svg.append("g")
            .attr("class", "legend");

        mySvg.selectAll("legendSquares")
            .data(data)
            .enter()
            .append("rect")
                .attr("x", x)
                .attr("y", (d, i) => y + i * (size + 5))
                .attr("width", size)
                .attr("height", size)
                .style("fill", d => domain(d));

        mySvg.selectAll("legendLabels")
            .data(data)
            .enter()
            .append("text")
            .attr("x", x + size * 1.2)
            .attr("y", (d, i) => y + i * (size + 5) + (size / 2))
            .style("fill", d => domain(d))
            .text(d => d)
            .attr("text-anchor", "left")
            .style("alignment-baseline", "middle");
    }
}

export default Legend;