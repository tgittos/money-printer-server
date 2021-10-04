import * as d3 from "d3";
import IAxisProps from "../../interfaces/IAxisProps";
import {Axis, ScaleLinear} from "d3";
import IAxis from "../../interfaces/IAxis";
import ITimeBasedDataPoint from "../../interfaces/ITimeBasedDataPoint";

class CandleXAxis implements IAxis<ITimeBasedDataPoint> {
    readonly props: IAxisProps<ITimeBasedDataPoint, Date>;

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
        const { width } = this.props.dimensions;
        const data = [].concat(this.props.data);

        this._scale = d3.scaleLinear()
            .domain([-1, data.length])
            .range([0, width]);
    }

    private createAxis() {
        const { dimensions } = this.props;
        const scale = this._scale;
        const data = [].concat(this.props.data);
        const svgWidth = dimensions.width - dimensions.margin.left - dimensions.margin.right;

        this._axis = d3.axisBottom(scale)
            .ticks(svgWidth / 80)
            .tickFormat(function(d, i) {
                const datum = data[d.valueOf()];
                if (datum) {
                    const date = datum.x;
                    const hours = date.getHours();
                    const minutes = (date.getMinutes()<10?'0':'') + date.getMinutes();
                    const seconds = date.getSeconds();
                    return `${hours}:${minutes}:${seconds}`
                };
                return '';
            });
    }
}

export default CandleXAxis;
