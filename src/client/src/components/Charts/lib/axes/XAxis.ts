import Axis, {IAxisProps} from "./Axis";
import * as d3 from "d3";
import IFigureDataPoint from "../../interfaces/IFigureDataPoint";

export interface IXAxisProps<T extends number | Date> extends IAxisProps<IFigureDataPoint, T> {
    tickCount?: number;
    tickFormatter?: (domain: d3.AxisDomain, idx: number) => string;
}

class XAxis<T extends number | Date> extends Axis<IFigureDataPoint, T> {

    protected _axis: d3.Axis<d3.AxisDomain>;

    constructor(props: IXAxisProps<T>) {
        super({
            ...props,
            axis: d3.axisBottom
        });

        this._axis = this.props.axis(this.props.scale)
            .ticks(props.tickCount)
            .tickFormat(props.tickFormatter);
    }

    draw(svg: d3.Selection<SVGElement, IFigureDataPoint[], HTMLElement, undefined>): void {
        const xAxis = this._axis;
        const { margin, height } = this.props.dimensions;

        console.log('drawing')

        svg.append("g")
            .attr("class", "axis x-axis") //Assign "axis" class
            .attr("transform", "translate(" + margin.left + "," + height + ")")
            .call(xAxis)
    }
}

export default XAxis;