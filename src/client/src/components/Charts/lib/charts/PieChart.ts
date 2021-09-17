import IChart from "../../interfaces/IChart";
import * as d3 from "d3";
import {MutableRefObject} from "react";
import Pie, {IPieData} from "../figures/Pie";
import IChartProps from "../../interfaces/IChartProps";
import IFigureProps from "../../interfaces/IFigureProps";
import Legend, {ILegendProps} from "../figures/Legend";
import {ScaleOrdinal} from "d3";

class PieChart implements IChart {
    readonly svg: d3.Selection<SVGElement, IPieData[], HTMLElement, undefined>;

    private props: IChartProps<IPieData>;
    private svgRef: MutableRefObject<null>;
    private colorDomain: ScaleOrdinal<any, any>;
    private pie: Pie;
    private legend: Legend;

    constructor(props: IChartProps<IPieData>) {
        this.props = props;
        this.svgRef = props.svgRef;
        this.svg = d3.select(this.svgRef.current);

        this.draw();
    }

    draw() {
        this.reset();

        this.pie.draw(this.svg);
        this.legend.draw(this.svg);
    }

    private init() {
        const { margin, width, height } = this.props.dimensions;
        const svgWidth = margin.left + margin.right + width;
        const svgHeight = margin.top + margin.bottom + height;

        const flatLabels = this.props.data.map(d => d.name);

        this.colorDomain = d3.scaleOrdinal()
            .domain(flatLabels)
            .range(d3.quantize(t => d3.interpolateSpectral(t), flatLabels.length).reverse());

        this.pie = new Pie({
            data: this.props.data,
            dimensions: this.props.dimensions,
            colorScale: this.colorDomain
        } as IFigureProps);

        this.legend = new Legend({
            labels: flatLabels.reverse(),
            domain: this.colorDomain
        } as ILegendProps);

        this.svg
            .attr("width", svgWidth)
            .attr("height", svgHeight)
            .append("g")
            .attr("transform", "translate(" +margin.left+ "," +margin.top+ ")");
    }

    private reset() {
        this.svg.selectAll('*').remove();
        this.init();
    }
}

export default PieChart;