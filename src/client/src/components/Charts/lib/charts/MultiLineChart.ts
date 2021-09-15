import IChartProps from "../../interfaces/IChartProps";
import * as d3 from "d3";
import Line, {ILineProps} from "../figures/Line";
import SimpleYAxis from "../axes/SimpleYAxis";
import IChart from "../../interfaces/IChart";
import {MutableRefObject} from "react";
import IAxis from "../../interfaces/IAxis";
import IFigureDataPoint from "../../interfaces/IFigureDataPoint";
import ILineDataPoint from "../../interfaces/ILineDataPoint";
import ITimeBasedDataPoint from "../../interfaces/ITimeBasedDataPoint";
import SimpleXAxis from "../axes/SimpleXAxis";
import moment from "moment";
import Legend from "../figures/Legend";
import {ScaleOrdinal} from "d3";

export interface IMultiLineChartDataEntry {
    name: string;
    data: ILineDataPoint[]
}

class MultiLineChart implements IChart {
    readonly svg: d3.Selection<SVGElement, ILineDataPoint[], HTMLElement, undefined>;

    private props: IChartProps<IMultiLineChartDataEntry>;
    private svgRef: MutableRefObject<null>;
    private xAxis: IAxis<ITimeBasedDataPoint>;
    private yAxis: IAxis<IFigureDataPoint>;
    private colorDomain: ScaleOrdinal<any, any>;
    private legend: Legend;
    private lines: Line[];

    constructor(props: IChartProps<IMultiLineChartDataEntry>) {
        this.props = props;
        this.svgRef = props.svgRef;
        this.svg = d3.select(this.svgRef.current);
        this.lines = [];

        this.draw();
    }

    public draw() {
        this.reset();

        this.xAxis.draw(this.svg);
        this.yAxis.draw(this.svg);

        this.lines.map(line => line.draw(this.svg));

        this.legend.draw(this.svg)
    }

    private init() {
        const { margin, width, height } = this.props.dimensions;
        const svgWidth = margin.left + margin.right + width;
        const svgHeight = margin.top + margin.bottom + height;

        // pull out axis data from all bundled sub data figures
        const flatLabels: string[] = [];
        const flatData = this.props.data.flatMap(entry => entry.data)
            .sort((a, b) => {
                return a.x < b.x
                    ? -1
                    : a.x > b.x
                        ? 1
                        : 0;
            });

        this.colorDomain = d3.scaleOrdinal()
            .domain(flatLabels)
            .range(d3.schemeSet1);

        this.xAxis = new SimpleXAxis({
            data: flatData,
            dimensions: this.props.dimensions,
            mapper: datum => moment.utc(datum.x).toDate()
        });
        this.yAxis = new SimpleYAxis({
            data: flatData,
            dimensions: this.props.dimensions,
            mapper: datum => datum.y
        });

        for (let i = 0; i < this.props.data.length; i++) {
            const fig = this.props.data[i] as IMultiLineChartDataEntry;
            this.lines.push(
                new Line({
                    name: fig.name,
                    data: fig.data,
                    dimensions: this.props.dimensions,
                    xScale: this.xAxis.scale,
                    yScale: this.yAxis.scale,
                    color: this.colorDomain(i)
                } as ILineProps));
            flatLabels.push(fig.name);
        }

        this.legend = new Legend({
            x: width - margin.right - 120,
            y: margin.top + 20,
            size: 10,
            domain: this.colorDomain,
            labels: flatLabels
        });

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

export default MultiLineChart;
