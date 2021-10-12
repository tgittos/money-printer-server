import Axis, {IAxisProps} from "./Axis";
import * as d3 from "d3";
import IFigureDataPoint from "../../interfaces/IFigureDataPoint";

export interface IXAxisProps<T extends (number | Date)> extends IAxisProps<IFigureDataPoint, T> {
    tickCount?: number;
    tickFormatter?: (domain: d3.AxisDomain, idx: number) => string;
    alignment?: "bottom" | "middle" | "top";
}

class XAxis<T extends (number | Date)> extends Axis<IFigureDataPoint, T> {

    protected props: IXAxisProps<T>
    protected _axis: d3.Axis<d3.AxisDomain>;

    constructor(props: IXAxisProps<T>) {
        super(props);
        this.props = props;

        this.props.alignment = this.props.alignment || "bottom";

        this._axis = this.props.axis(this.props.scale)
            .ticks(this.props.tickCount)
            .tickFormat(this.props.tickFormatter);
    }

    draw(svg: d3.Selection<SVGElement, IFigureDataPoint[], HTMLElement, undefined>): void {
        const xAxis = this._axis;
        const { dimensions: { margin, height }, alignment } = this.props;

        const offset = alignment === "top"
            ? -height + margin.top
            : alignment === "middle"
                ? -height / 2
                : 0;

        svg.append("g")
            .attr("class", "axis x-axis") //Assign "axis" class
            .attr("transform", "translate(" + margin.left + "," + (height + offset) + ")")
            .call(xAxis)
    }
}

export default XAxis;