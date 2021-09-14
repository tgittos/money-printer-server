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
    }

    private init() {
        const { margin, width, height } = this.props.dimensions;
        const svgWidth = margin.left + margin.right + width;
        const svgHeight = margin.top + margin.bottom + height;

        // pull out axis data from all bundled sub data figures
        const flatData = this.props.data.flatMap(entry => entry.data)
            .sort((a, b) => {
                return a.x < b.x
                    ? -1
                    : a.x > b.x
                        ? 1
                        : 0;
            });

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
            console.log('creating line for figure:', fig);
            this.lines.push(
                new Line({
                    name: fig.name,
                    data: fig.data,
                    dimensions: this.props.dimensions,
                    xScale: this.xAxis.scale,
                    yScale: this.yAxis.scale
                } as ILineProps));
        }

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
