import * as d3 from "d3";
import IAxisProps from "../../interfaces/IAxisProps";
import {Axis, ScaleTime} from "d3";
import IAxis from "../../interfaces/IAxis";
import ITimeBasedDataPoint from "../../interfaces/ITimeBasedDataPoint";

class SimpleXAxis implements IAxis<ITimeBasedDataPoint> {
    readonly props: IAxisProps<ITimeBasedDataPoint, Date>;

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

    constructor(props: IAxisProps<ITimeBasedDataPoint, Date>) {
        this.props = props;

        this.createScale();
        this.createAxis();
    }

    public draw(svg: d3.Selection<SVGElement, ITimeBasedDataPoint[], HTMLElement, undefined>) {
        const xAxis = this._axis;
        const { margin, height } = this.props.dimensions;

        svg.append("g")
            .attr("class", "axis x-axis") //Assign "axis" class
            .attr("transform", "translate(" + margin.left + "," + height + ")")
            .call(xAxis)
    }

    private createScale() {
        const { dimensions, mapper } = this.props;
        const { width } = dimensions;
        const data = [].concat(this.props.data) as ITimeBasedDataPoint[];

        const timeExtent = d3.extent(data, mapper);

        this._scale = d3.scaleTime()
            .domain(timeExtent)
            .range([0, width]);
    }

    private createAxis() {
        const { dimensions } = this.props;
        const scale = this._scale;

        const svgWidth = dimensions.width - dimensions.margin.left - dimensions.margin.right;

        this._axis = d3.axisBottom(scale)
            .ticks(svgWidth / 30)
            .tickFormat(d3.timeFormat('%m/%y'));
    }
}

export default SimpleXAxis;
