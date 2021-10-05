import Axis, {IAxisProps} from "./Axis";
import * as d3 from "d3";
import IFigureDataPoint from "../../interfaces/IFigureDataPoint";

export interface IYAxisProps extends IAxisProps<IFigureDataPoint, number>{
    tickCount?: number;
    tickFormatter?: (domain: d3.AxisDomain, idx: number) => string | null;
}

class YAxis extends Axis<IFigureDataPoint, number> {

    protected _axis: d3.Axis<d3.AxisDomain>;

    constructor(props: IYAxisProps) {
        super(props);

        // set the tick format
        this._axis = this.props.axis(this.props.scale)
            .ticks(props.tickCount)
            .tickFormat(props.tickFormatter);
    }

    draw(svg: d3.Selection<SVGElement, IFigureDataPoint[], HTMLElement, undefined>): void {
        const yAxis = this._axis;
        const { margin, height } = this.props.dimensions;

        svg.append("g")
            .attr("class", "axis y-axis") //Assign "axis" class
            .attr("transform", "translate(" + margin.left + ", 0)")
            .call(yAxis)
    }
}

export default YAxis;