import styles from './InvestmentPerformance.module.scss';
import React, {FormEvent} from "react";
import BasicCandleChart from "../../Charts/lib/charts/BasicCandleChart";
import Holding from "../../../models/Holding";
import StockService from "../../../services/StockService";
import HistoricalIntradaySymbol, {IHistoricalIntradaySymbol} from "../../../models/symbols/HistoricalIntradaySymbol";
import BigLoader from "../../shared/Loaders/BigLoader";
import ICandleDataPoint from "../../Charts/interfaces/ICandleDataPoint";
import IChartDimensions from "../../Charts/interfaces/IChartDimensions";
import StaticChart from "../../Charts/StaticChart";
import moment from "moment";
import HistoricalEoDSymbol, {IHistoricalEoDSymbol} from "../../../models/symbols/HistoricalEoDSymbol";
import {Dropdown} from "react-bootstrap";
import {IChartFactory} from "../../Charts/lib/ChartFactory";
import Candle from "../../Charts/lib/figures/Candle";
import BasicLineChart from "../../Charts/lib/charts/BasicLineChart";

export interface IInvestmentPerformanceProps {
    holding: Holding;
}

export interface IInvestmentPerformanceState {
    loading: boolean;
    activeChart: IChartFactory;
    // todo - gross
    activeChartType: string;
    intradayData: IHistoricalIntradaySymbol[];
    eodData: IHistoricalEoDSymbol[];
}

class InvestmentPerformance extends React.Component<IInvestmentPerformanceProps, IInvestmentPerformanceState> {

    private _stocks: StockService;

    private get lastWeek(): Date {
        const lastWeek = moment().subtract(1, 'weeks').toDate();
        return lastWeek;
    }

    constructor(props: IInvestmentPerformanceProps) {
        super(props);

        this.state = {
            loading: true,
            intradayData: [],
            eodData: [],
            activeChart: BasicCandleChart,
            activeChartType: 'Candle'
        };

        this._onHistoricalIntradayDataReceived = this._onHistoricalIntradayDataReceived.bind(this);
        this._onHistoricalEoDDataReceived = this._onHistoricalEoDDataReceived.bind(this);
        this._onChartTypeChanged = this._onChartTypeChanged.bind(this);

        this._stocks = new StockService();
    }

    componentDidMount() {
        this._stocks.historicalIntraday(this.props.holding.securitySymbol, this.lastWeek)
            .then(this._onHistoricalIntradayDataReceived);
    }

    componentDidUpdate(prevProps: Readonly<IInvestmentPerformanceProps>,
                       prevState: Readonly<IInvestmentPerformanceState>, snapshot?: any) {
        const prevHolding = prevProps.holding;
        const newHolding = this.props.holding;

        if (prevHolding && newHolding && prevHolding?.id != newHolding?.id) {
            // re-fetch data from the server
            const lastWeek = moment().subtract(1, 'weeks').toDate();
            this._stocks.historicalIntraday(this.props.holding.securitySymbol, this.lastWeek)
                .then(this._onHistoricalIntradayDataReceived);
        }
    }

    private _onHistoricalIntradayDataReceived(data: IHistoricalIntradaySymbol[]) {
        if (data && data.length == 0) {
            // no data from the intraday, maybe this symbol only supports closing daily prices
            // ie - it's a mutual fund or something
            this._stocks.historicalEoD(this.props.holding.securitySymbol, this.lastWeek)
                .then(this._onHistoricalEoDDataReceived);
        }
        this.setState(prev => ({
            ...prev,
            intradayData: data.map(datum => new HistoricalIntradaySymbol(this.props.holding.securitySymbol, datum)),
            loading: false
        }));
    }

    private _onHistoricalEoDDataReceived(data: IHistoricalEoDSymbol[]) {
        if (data && data.length == 0) {
            // no data from the EoD endpoint either, hmmm
            console.log("InvestmentPerformance - unable to find either intraday or EoD data for this symbol",
                this.props.holding);
            this.setState(prev => ({
                ...prev,
                loading: false
            }));
        }
        this.setState(prev => ({
            ...prev,
            eodData: data.map(datum => new HistoricalEoDSymbol(this.props.holding.securitySymbol, datum)),
            loading: false
        }));
    }

    private _onChartTypeChanged(chartType: string | undefined) {
        console.log('chart type:', chartType)
        if (chartType) {
            this.setState(prev => ({
                ...prev,
                activeChartType: chartType
            }));
        }
    }

    private get _chartType(): IChartFactory {
        const { activeChartType } = this.state;
        if (activeChartType === 'Candle') {
            return BasicCandleChart;
        }
        if (activeChartType === 'Line') {
            return BasicLineChart;
        }
    }

    private _formatDataForCandle() {
        const { intradayData, eodData } = this.state;

        let data = intradayData;
        if (data.length === 0) {
            data = eodData;
        };

        const formattedData = data.map(datum => {
            return {
                x: datum.date,
                open: datum.open,
                close: datum.close,
                high: datum.high,
                low: datum.low,
            } as ICandleDataPoint;
        });

        return formattedData;
    }

    render() {
        if (this.state.loading) {
            return <BigLoader></BigLoader>
        }

        return <div className={styles.InvestmentPerformance}>
            <h1>{ this.props.holding.securitySymbol }</h1>

            <div>
                <div className="chart-controls">
                    <Dropdown onSelect={this._onChartTypeChanged}>
                        <Dropdown.Toggle>
                            Chart: { this.state.activeChartType }
                        </Dropdown.Toggle>
                        <Dropdown.Menu>
                            <Dropdown.Item eventKey='Candle'>Candle</Dropdown.Item>
                            <Dropdown.Item eventKey='Line'>Line</Dropdown.Item>
                        </Dropdown.Menu>
                    </Dropdown>
                </div>
            </div>

            <StaticChart chart={this._chartType}
                     dimensions={{
                         width: 1000,
                         height: 700,
                         margin: {
                             top: 5,
                             bottom: 25,
                             left: 35,
                             right: 5
                         }
                     } as IChartDimensions}
                     data={this._formatDataForCandle()}
                     ticker={this.props.holding.securitySymbol}
            />
        </div>
    }
}

export default InvestmentPerformance;
