import * as d3 from "d3";
import IAxisProps from "../../interfaces/IAxisProps";
import {Axis, ScaleLinear } from "d3";
import IAxis from "../../interfaces/IAxis";
import IFigureDataPoint from "../../interfaces/IFigureDataPoint";

class SimpleYAxis implements IAxis<IFigureDataPoint> {
    readonly props: IAxisProps<IFigureDataPoint, number>;

    private _scale: ScaleLinear<any, any>
    private _axis: Axis<any>;

    public get scale(): ScaleLinear<any, any> {
        return this._scale;
    }

    public get axis(): Axis<any> {
        return this._axis;
    }

    constructor(props: IAxisProps<IFigureDataPoint, number>) {
        this.props = props;

        this._createScale();
        this._createAxis();
    }

    public draw(svg: d3.Selection<SVGElement, IFigureDataPoint[], HTMLElement, undefined>) {
        const yAxis = this._axis;
        const { margin  } = this.props.dimensions;

        svg.append("g")
            .attr("class", "axis y-axis")
            .attr("transform", "translate(" + margin.left + ", 0)")
            .call(yAxis);
    }

    private _createScale() {
        const { mapper, dimensions } = this.props;
        const { height } = dimensions;

        const extent = d3.extent(this.props.data, mapper);

        this._scale = d3.scaleLinear()
            .domain([extent[0], extent[1] + extent[1] * 0.1])
            .range([height, 0]);
    }

    private _createAxis() {
        const scale = this._scale;

        this._axis = d3.axisLeft(scale);
    }
}

export default SimpleYAxis;
