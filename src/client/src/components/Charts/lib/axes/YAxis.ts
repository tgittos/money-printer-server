import * as d3 from "d3";
import BaseAxis from "../base/BaseAxis";

class YAxis extends BaseAxis {

    protected createScale() {
        const { data, chartHeight, scale } = this._props;

        const yMin = d3.min(data.map(r => r.low));
        const yMax = d3.max(data.map(r => r.high));

        this._scale = scale().domain([yMin, yMax]).range([chartHeight, 0]).nice();
    }

    protected override createAxis() {
        const scale = this._scale;
        this._axis =  d3.axisLeft().scale(scale);
    }


    public override draw(svg: d3.Selection<SVGGElement, unknown, null, undefined>) {
        const axis = this._axis;
        const gY = svg.append("g")
            .attr("class", "axis y-axis")
            .call(axis);
    }
}

export default YAxis;
