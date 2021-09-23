import IFigureProps from "../../interfaces/IFigureProps";
import * as d3 from "d3";
import IFigureDataPoint from "../../interfaces/IFigureDataPoint";
import {PieArcDatum, ScaleOrdinal} from "d3";

export interface IPieData extends IFigureDataPoint{
    name: string;
    value: number;
}

export interface IPieProps extends IFigureProps {
    labelFormatter?: (val: IPieData) => string;
    valueFormatter?: (val: IPieData) => string;
}

class Pie {
    readonly props: IPieProps;
    readonly colorDomain: ScaleOrdinal<any, any>;
    readonly labelFormatter: (val: IPieData) => string;
    readonly valueFormatter: (val: IPieData) => string | number;

    constructor(props: IPieProps) {
        this.props = props;
        this.colorDomain = this.props.colorScale;

        this.labelFormatter = this.props.labelFormatter ??
            ((datum: IPieData) => datum.name);
        this.valueFormatter = this.props.valueFormatter ??
            ((datum: IPieData) => datum.value);
    }

    public draw(svg: d3.Selection<SVGElement, IPieData[], HTMLElement, undefined>) {
        const {data, dimensions} = this.props;
        const {margin, width, height} = dimensions;

        const radius = Math.min(width, height) / 2 * 0.8;

        const color = this.colorDomain ?? d3.scaleOrdinal()
            .domain((this.props.data as IPieData[]).map(d => d.name))
            .range(d3.quantize(t => d3.interpolateSpectral(t * 0.8 + 0.1), data.length).reverse());

        const arc = d3.arc<PieArcDatum<IPieData>>()
            .innerRadius(0)
            .outerRadius(Math.min(width, height / 2 - 1));

        const arcLabel = d3.arc<PieArcDatum<IPieData>>()
            .innerRadius(radius)
            .outerRadius(radius);

        const pie = d3.pie<IPieData>()
            .value(d => d.value);

        const arcs = pie(data as IPieData[]);

        const mySvg = svg.append("g")
            .attr("class", "pie")
            .attr("transform", "translate(" + width / 2 + "," + height / 2 + ")");

        mySvg.append("g")
            .attr("stroke", "white")
            .selectAll("path")
            .data(arcs)
            .join("path")
                .attr("fill", d => color(d.data.name))
                .attr("d", arc)
            .append("title")
                .text(d => `${d.data.name}: ${d.data.value}`);

        mySvg.append("g")
            .attr("font-family", "sans-serif")
            .attr("font-size", 12)
            .attr("text-anchor", "middle")
            .selectAll("text")
            .data(arcs)
            .join("text")
            .attr("transform", d => `translate(${arcLabel.centroid(d)})`)
            .call(text => text.filter(d => (d.endAngle - d.startAngle) > 0.25).append("tspan")
                .attr("y", "-0.4em")
                .attr("font-weight", "bold")
                .text(d => this.labelFormatter(d.data)))
            .call(text => text.filter(d => (d.endAngle - d.startAngle) > 0.25).append("tspan")
                .attr("x", 0)
                .attr("y", "0.7em")
                .attr("fill-opacity", 0.7)
                .text(d => this.valueFormatter(d.data)));
    }
}

export default Pie;
