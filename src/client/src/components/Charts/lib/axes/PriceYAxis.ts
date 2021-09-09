import * as d3 from "d3";
import Symbol from "../../../../models/Symbol";
import IAxisProps from "../../interfaces/IAxisProps";
import {Axis, ScaleLinear } from "d3";
import IAxis from "../../interfaces/IAxis";

class PriceYAxis implements IAxis {
    readonly props: IAxisProps;

    private _scale: ScaleLinear<any, any>
    private _axis: Axis<any>;

    public get scale(): ScaleLinear<any, any> {
        return this._scale;
    }

    public get axis(): Axis<any> {
        return this._axis;
    }

    constructor(props: IAxisProps) {
        this.props = props;

        this._createScale();
        this._createAxis();
    }

    public draw(svg: d3.Selection<SVGElement, Symbol[], HTMLElement, undefined>) {
        const yAxis = this._axis;
        const { margin  } = this.props.dimensions;

        svg.append("g")
            .attr("class", "axis y-axis")
            .attr("transform", "translate(" + margin.left + ", 0)")
            .call(yAxis);
    }

    private _createScale() {
        const { height } = this.props.dimensions;

        const yMin = d3.min(this.props.data, (s: Symbol) => +s.week52Low);
        const yMax = d3.max(this.props.data, (s: Symbol) => +s.week52High);

        this._scale = d3.scaleLinear()
            .domain([yMin, yMax + yMax * 0.1])
            .range([height, 0]);
    }

    private _createAxis() {
        const scale = this._scale;

        this._axis = d3.axisLeft(scale);
    }
}

export default PriceYAxis;
