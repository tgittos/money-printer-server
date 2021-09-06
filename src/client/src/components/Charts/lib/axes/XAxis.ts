import * as d3 from "d3";
import BaseAxis from "../base/BaseAxis";
import moment from "moment";

class XAxis extends BaseAxis{

    private get _dates(): Date[] {
        const { data } = this._props;
        return data.map(datum => datum.date);
    }

    protected override createScale() {
        const { chartWidth, scale } = this._props;
        const dates = this._dates;

        console.log('dates:', dates);

        this._scale = scale()
            //.domain(d3.extent(dates))
            .domain([-1, dates.length])
            .range([0, chartWidth])
    }

    protected override createAxis() {
        const scale = this._scale;
        const dates = this._dates;

        this._axis = d3.axisBottom()
            .scale(scale)
            .tickFormat(function (d) {
                    console.log(dates[d]);
                    const date = new Date(dates[d]);
                    console.log("date:", date);
                return moment(date).format("YYYY/MM/DD h:mm:ss a")
            });
    }

    public override draw(svg: d3.Selection<SVGGElement, unknown, null, undefined>) {
        const { chartHeight } = this._props;
        const axis = this._axis;
        const gX = svg.append("g")
            .attr("class", "axis x-axis") //Assign "axis" class
            .attr("transform", "translate(0," + chartHeight + ")")
            .call(axis)
    }
}

export default XAxis;
