import Axis, {IAxisProps} from "./Axis";
import * as d3 from "d3";
import IFigureDataPoint from "../../interfaces/IFigureDataPoint";

export interface IXAxisProps<T, U extends number | Date> extends IAxisProps<T, U> {
    tickCount?: number;
    tickFormatter?: (domain: d3.AxisDomain, idx: number) => string;
}

class XAxis<T extends number | Date> extends Axis<IFigureDataPoint, T> {

    constructor(props: IXAxisProps<IFigureDataPoint, T>) {
        super({
            ...props,
            axis: d3.axisBottom
        });

        // set the tick format
        this._axis
            .ticks(props.tickCount)
            .tickFormat(props.tickFormatter);
    }

    draw(svg: d3.Selection<SVGElement, IFigureDataPoint[], HTMLElement, undefined>): void {
        const xAxis = this._axis;
        const { margin, height } = this.props.dimensions;

        svg.append("g")
            .attr("class", "axis x-axis") //Assign "axis" class
            .attr("transform", "translate(" + margin.left + "," + height + ")")
            .call(xAxis)
    }
}

export default XAxis;