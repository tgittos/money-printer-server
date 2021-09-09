import * as d3 from "d3";
import Symbol from "../../../../models/Symbol";
import IAxisProps from "../../interfaces/IAxisProps";
import moment from "moment";
import {Axis, ScaleTime} from "d3";
import IAxis from "../../interfaces/IAxis";

class RealtimeXAxis implements IAxis {
    readonly props: IAxisProps;

    private _scale: ScaleTime<any, any>;
    private _axis: Axis<any>;

    public get scale(): ScaleTime<any, any> {
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
        const xAxis = this._axis;
        const { margin, height } = this.props.dimensions;

        svg.append("g")
            .attr("class", "axis x-axis") //Assign "axis" class
            .attr("transform", "translate(" + margin.left + "," + height + ")")
            .call(xAxis)
    }

    private _createScale() {
        const { width } = this.props.dimensions;
        const now = new Date();

        now.setMinutes(now.getMinutes() + 15);
        const windowStart = moment(now).subtract(1, 'hour');

        this._scale = d3.scaleTime()
            .domain([windowStart, now])
            .range([0, width]);
    }

    private _createAxis() {
        const scale = this._scale;
        
        this._axis = d3.axisBottom(scale)
            .ticks(d3.timeMinute.every(2))
            .tickFormat(d3.timeFormat('%H:%M'));
    }
}

export default RealtimeXAxis;
