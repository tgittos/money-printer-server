import * as d3 from "d3";
import IAxisProps from "../../interfaces/IAxisProps";
import moment from "moment";
import {Axis, ScaleTime} from "d3";
import IAxis from "../../interfaces/IAxis";
import ISymbol from "../../../../interfaces/ISymbol";

class RealtimeXAxis implements IAxis {
    readonly props: IAxisProps;

    private _scale: ScaleTime<any, any>;
    private _axis: Axis<any>;

    public get scale(): ScaleTime<any, any> {
        return this._scale;
    }

    public get domain(): Date[] {
        return this._scale.domain();
    }

    public get axis(): Axis<any> {
        return this._axis;
    }

    constructor(props: IAxisProps) {
        this.props = props;

        this._createScale();
        this._createAxis();
    }

    public draw(svg: d3.Selection<SVGElement, ISymbol[], HTMLElement, undefined>) {
        const xAxis = this._axis;
        const { margin, height } = this.props.dimensions;

        svg.append("g")
            .attr("class", "axis x-axis") //Assign "axis" class
            .attr("transform", "translate(" + margin.left + "," + height + ")")
            .call(xAxis)
    }

    private _createScale() {
        const { width } = this.props.dimensions;

        const timeExtent = d3.extent(this.props.data,
            (s: ISymbol) => s.date);

        this._scale = d3.scaleTime()
            .domain(timeExtent)
            .range([0, width]);
    }

    private _createAxis() {
        const scale = this._scale;
        
        this._axis = d3.axisBottom(scale)
            .tickFormat(d3.timeFormat('%H:%M'));
    }
}

export default RealtimeXAxis;
