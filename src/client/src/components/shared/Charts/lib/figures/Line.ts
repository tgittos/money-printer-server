import * as d3 from "d3";
import IFigureProps from "../../interfaces/IFigureProps";
import ILineDataPoint from "../../interfaces/ILineDataPoint";
import moment from "moment";
import {ScaleOrdinal} from "d3";

export interface ILineProps extends IFigureProps {
    data: ILineDataPoint[]
    color: string;
}

class Line<T extends ILineDataPoint> {
    readonly props: ILineProps;

    constructor(props: ILineProps) {
        this.props = props;
    }

    public draw(svg: d3.Selection<SVGElement, ILineDataPoint[], HTMLElement, undefined>) {
        const { xScale, yScale, color, dimensions } = this.props;
        const { margin } = dimensions;

        const lineGenerator = d3.line<ILineDataPoint>()
            // this filtering by 0 thing is kinda dodgy
            .defined(d => d !== undefined && !isNaN(d.y) && d.y > 0)
            .x((d) => {
                return xScale(d.x);
            })
            .y((d) => {
                return yScale(d.y);
            });

        svg.append("g")
                .attr("transform", "translate(" +margin.left+ "," +margin.top+ ")")
            .append("path")
            .datum(this.props.data)
            .attr("fill", "none")
            .attr("stroke", (d, i) => color ?? "#6dc98f")
            .attr("stroke-width", 1.5)
            .attr("d", lineGenerator);
    }
}
class BasicLine extends Line<ILineDataPoint> {}

export default BasicLine;
