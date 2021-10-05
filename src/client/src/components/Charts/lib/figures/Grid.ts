import * as d3 from "d3";
import IFigureDataPoint from "../../interfaces/IFigureDataPoint";
import IChartDimensions from "../../interfaces/IChartDimensions";

export interface IGridProps {
    dimensions: IChartDimensions;
    xDomain: any;
    yDomain: any;
}

class Grid {
    readonly props: IGridProps;

    constructor(props: IGridProps) {
        this.props = props;
    }

    public draw(svg: d3.Selection<SVGElement, IFigureDataPoint[], HTMLElement, undefined>) {
        const { xDomain, yDomain, dimensions } = this.props
        const { height, width, margin } = dimensions;

        const mySvg = svg.append("g")
            .attr("class", "grid");

        mySvg.attr("stroke", "currentColor")
            .attr("stroke-opacity", 0.1)
            .call(g => g.append("g")
                .selectAll("line")
                .data(xDomain.ticks())
                .join("line")
                .attr("x1", d => 0.5 + xDomain(d))
                .attr("x2", d => 0.5 + xDomain(d))
                .attr("y1", margin.top)
                .attr("y2", height - margin.bottom))
            .call(g => g.append("g")
                .selectAll("line")
                .data(yDomain.ticks())
                .join("line")
                .attr("y1", d => 0.5 + yDomain(d))
                .attr("y2", d => 0.5 + yDomain(d))
                .attr("x1", margin.left)
                .attr("x2", width - margin.right));
    }
}

export default Grid;
