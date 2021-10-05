import IChartProps from "../../interfaces/IChartProps";
import * as d3 from "d3";
import Candle, {ICandleProps} from "../figures/Candle";
import IChart from "../../interfaces/IChart";
import {MutableRefObject} from "react";
import {ScaleBand} from "d3";
import ICandleDataPoint from "../../interfaces/ICandleDataPoint";
import XAxis from "../axes/XAxis";
import YAxis from "../axes/YAxis";
import moment from "moment";

class BasicCandleChart implements IChart {
    readonly svg: d3.Selection<SVGElement, ICandleDataPoint[], HTMLElement, undefined>;

    private props: IChartProps<ICandleDataPoint>;
    private svgRef: MutableRefObject<null>;
    private xAxis: XAxis<Date>;
    private yAxis: YAxis;
    private xBand: ScaleBand<any>;
    private candles: Candle;

    constructor(props: IChartProps<ICandleDataPoint>) {
        this.props = props;
        this.svgRef = props.svgRef;
        this.svg = d3.select(this.svgRef.current);

        if (this.props.data) {
            this.draw();
        } else {
            console.log('BasicCandleChart::constructor - cannot render chart, no data found');
        }
    }

    public draw() {
        this.reset();

        this.xAxis.draw(this.svg);
        this.yAxis.draw(this.svg);

        this.candles.draw(this.svg);
    }

    private init() {
        const { margin, width, height } = this.props.dimensions;
        const svgWidth = margin.left + margin.right + width;
        const svgHeight = margin.top + margin.bottom + height;

        const mapper =

        this.xAxis = new XAxis<Date>({
            data: this.props.data,
            dimensions: this.props.dimensions,
            scale: d3.scaleTime,
            axis: d3.axisBottom,
            mapper: (datum: ICandleDataPoint, idx: number, arr: ICandleDataPoint[]) => datum.date,
            tickFormatter: (d, i) => {
                const date = moment.utc(d.valueOf());
                return date.format("");
            }
        });

        this.yAxis = new YAxis({
            data: this.props.data,
            dimensions: this.props.dimensions,
            scale: d3.scaleLinear,
            axis: d3.axisLeft,
            mapper: (datum: ICandleDataPoint, idx: number, arr: ICandleDataPoint[]) => datum?.close,
        });

        this.xBand = d3.scaleBand<number>()
            .domain(d3.range(-1, this.props.data.length))
            .range([0, width])
            .padding(0.3)

        this.candles = new Candle({
            data: this.props.data,
            xScale: this.xAxis.scale,
            yScale: this.yAxis.scale,
            xBand: this.xBand,
            dimensions: this.props.dimensions
        } as ICandleProps);

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

export default BasicCandleChart;