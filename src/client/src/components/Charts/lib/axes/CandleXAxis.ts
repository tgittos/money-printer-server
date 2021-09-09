import * as d3 from "d3";
import Symbol from "../../../../models/Symbol";
import IAxisProps from "../../interfaces/IAxisProps";
import moment from "moment";
import {Axis, ScaleLinear, ScaleTime} from "d3";
import IAxis from "../../interfaces/IAxis";

class CandleXAxis implements IAxis {
    readonly props: IAxisProps;

    private _scale: ScaleLinear<any, any>;
    private _axis: Axis<any>;

    public get scale(): ScaleLinear<any, any> {
        return this._scale;
    }

    public get domain(): number[] {
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

        this._scale = d3.scaleLinear()
            .domain([-1, this.props.data.length])
            .range([0, width]);
    }

    private _createAxis() {
        const scale = this._scale;
        const data = this.props.data;

        this._axis = d3.axisBottom(scale)
            .ticks(d3.timeMinute.every(2))
            .tickFormat(function(d) {
                const date = data[d.valueOf()].date;
                console.log(date);
                const hours = date.getHours()
                const minutes = (date.getMinutes()<10?'0':'') + date.getMinutes()
                const amPM = hours < 13 ? 'am' : 'pm'
                return hours + ':' + minutes + amPM + ' ' + date.getDate() + ' ' + date.getFullYear()
            });
    }
}

export default CandleXAxis;
