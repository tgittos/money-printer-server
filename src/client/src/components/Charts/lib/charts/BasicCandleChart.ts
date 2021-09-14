import IChartProps from "../../interfaces/IChartProps";
import * as d3 from "d3";
import SimpleYAxis from "../axes/SimpleYAxis";
import Candle, {ICandleProps} from "../figures/Candle";
import CandleXAxis from "../axes/CandleXAxis";
import IChart from "../../interfaces/IChart";
import {MutableRefObject} from "react";
import IAxis from "../../interfaces/IAxis";
import {ScaleBand} from "d3";
import ICandleDataPoint from "../../interfaces/ICandleDataPoint";
import IFigureDataPoint from "../../interfaces/IFigureDataPoint";

class BasicCandleChart implements IChart {
    readonly svg: d3.Selection<SVGElement, ICandleDataPoint[], HTMLElement, undefined>;

    private props: IChartProps<ICandleDataPoint>;
    private svgRef: MutableRefObject<null>;
    private xAxis: IAxis<ICandleDataPoint>;
    private yAxis: IAxis<IFigureDataPoint>;
    private xBand: ScaleBand<any>;
    private candles: Candle;

    constructor(props: IChartProps<ICandleDataPoint>) {
        this.props = props;
        this.svgRef = props.svgRef;
        this.svg = d3.select(this.svgRef.current);

        this.props.data = this.props.data.reverse();

        this.draw();
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


        this.xAxis = new CandleXAxis({
            data: this.props.data,
            dimensions: this.props.dimensions,
            mapper: (data: ICandleDataPoint) => data.x
        });
        this.yAxis = new SimpleYAxis({
            data: this.props.data,
            dimensions: this.props.dimensions,
            mapper: (data: ICandleDataPoint) => data.close
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