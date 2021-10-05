import IChartProps from "../../interfaces/IChartProps";
import * as d3 from "d3";
import Candle, {ICandleProps} from "../figures/Candle";
import IChart from "../../interfaces/IChart";
import {MutableRefObject} from "react";
import ICandleDataPoint from "../../interfaces/ICandleDataPoint";
import XAxis, {IXAxisProps} from "../axes/XAxis";
import YAxis, {IYAxisProps} from "../axes/YAxis";
import moment from "moment";

class BasicCandleChart implements IChart {
    readonly svg: d3.Selection<SVGElement, ICandleDataPoint[], HTMLElement, undefined>;

    private props: IChartProps<ICandleDataPoint>;
    private svgRef: MutableRefObject<null>;
    private xScale: d3.ScaleTime<number, Date>
    private yScale: d3.ScaleLinear<number, number>
    private xBand: d3.ScaleBand<any>;
    private xAxis: XAxis<Date>;
    private yAxis: YAxis;
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

        const xMapper = (datum: ICandleDataPoint, idx: number, arr: ICandleDataPoint[]) => datum.date;
        const yMapper = (datum: ICandleDataPoint, idx: number, arr: ICandleDataPoint[]) => datum.close;

        const dateDomain = this.props.data.map(xMapper);
        const valDomain = this.props.data.map(yMapper);

        this.xScale = d3.scaleTime(d3.extent(dateDomain), [0, width]);
        this.xBand = d3.scaleBand<number>([0, dateDomain.length], [0, width])
            .padding(0.3);
        this.yScale = d3.scaleLinear(valDomain, [height, 0]);

        this.xAxis = new XAxis<Date>({
            data: this.props.data,
            dimensions: this.props.dimensions,
            scale: this.xScale,
            axis: d3.axisBottom,
            mapper: xMapper,
            tickFormatter: (d, i) => {
                const date = moment.utc(d.valueOf());
                return date.format();
            }
        } as IXAxisProps<Date>);

        this.yAxis = new YAxis({
            data: this.props.data,
            dimensions: this.props.dimensions,
            scale: this.yScale,
            axis: d3.axisLeft,
            mapper: yMapper
        } as IYAxisProps);


        this.candles = new Candle({
            data: this.props.data,
            xScale: this.xScale,
            yScale: this.yScale,
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