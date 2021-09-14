import * as d3 from "d3";
import IFigureProps from "../../interfaces/IFigureProps";
import ILineDataPoint from "../../interfaces/ILineDataPoint";
import moment from "moment";

export interface ILineProps extends IFigureProps {
    data: ILineDataPoint[]
}

class Line<T extends ILineDataPoint> {
    readonly props: ILineProps;

    constructor(props: ILineProps) {
        this.props = props;
    }

    public draw(svg: d3.Selection<SVGElement, ILineDataPoint[], HTMLElement, undefined>) {
        const { xScale, yScale, dimensions } = this.props;
        const { margin } = dimensions;

        const lineGenerator = d3.line<ILineDataPoint>()
            .x((d) => {
                const parsedDate = moment(d.x);
                const val = xScale(parsedDate);
                return val;
            })
            .y((d) => {
                const val = yScale(d.y);
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
class BasicLine extends Line<ILineDataPoint> {}

export default BasicLine;
