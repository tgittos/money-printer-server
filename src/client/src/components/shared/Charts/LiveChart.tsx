import React, {MutableRefObject} from 'react';
import {filter, Subscription} from "rxjs";

import BigLoader from "../Loaders/BigLoader";
import StaticChart from "./StaticChart";
import IChartDimensions from "./interfaces/IChartDimensions";
import {IChartFactory} from "./lib/ChartFactory";
import moment from 'moment';
import Env from "../../../env";
import ISymbol from "../../../interfaces/ISymbol";
import { SortDescending } from "../../../interfaces/ISymbol";
import StockService from "../../../services/StockService";
import {IHistoricalIntradaySymbol} from "../../../models/symbols/HistoricalIntradaySymbol";

interface ILiveChartProps {
    ticker: string;
    chart: IChartFactory;
    svgRef?: MutableRefObject<null>;
    dimensions: IChartDimensions;
    start?: Date;
    end?: Date;
}

interface ILiveChartState {
    loadingRealtime: boolean;
    loadingHistorical: boolean;
    cachedRealtimeData: ISymbol[];
    cachedHistoricalData: ISymbol[];
    chartData: ISymbol[];
    activeChartType: IChartFactory;
    start: Date;
    end?: Date;
}

class LiveChart extends React.Component<ILiveChartProps, ILiveChartState> {

    private _stocks: StockService;
    private _subscriptions: Subscription[] = [];

    private get loading(): boolean {
        return this.state.loadingHistorical || this.state.loadingRealtime
    }

    constructor(props: ILiveChartProps) {
        super(props);

        this.state = {
            loadingHistorical: true,
            loadingRealtime: true,
            cachedHistoricalData: [],
            cachedRealtimeData: [],
            chartData: [],
            start: props.start ?? moment().subtract(1, 'days'),
            activeChartType: this.props.chart
        } as ILiveChartState;

        this._onLiveData = this._onLiveData.bind(this);
        this._onHistoricalData = this._onHistoricalData.bind(this);

        this._stocks = new StockService();
    }

    componentDidMount() {
        this._subscriptions.push(
            this._stocks.connected$.subscribe(connected => {
                if (connected) {
                    if (Env.DEBUG) {
                        console.log('LiveChart::componentDidMount - connected to live quotes, subscribing to stream')
                    }
                    this._subscriptions.push(
                        this._stocks.liveQuotes$
                            .pipe(filter(val => val !== undefined))
                            .subscribe(this._onLiveData)
                    );
                    // subscribe to this ticker on the data upstream
                    this._stocks.subscribeToSymbol(this.props.ticker);
                    const yesterday: Date = moment().utc().subtract(7, 'days').toDate()
                    if (Env.DEBUG) {
                        console.log('LiveChart::componentDidMount - fetching historical data for ticker');
                    }
                    // this._stocks.historicalIntraday(this.props.ticker, yesterday)
                    //    .then(this._onHistoricalData);
                }
            })
        );
        this.setState(prev => ({
            ...prev,
            loading: false
        }))
    }

    componentWillUnmount() {
        // unsubscribe to the upstream symbol
        this._stocks.unsubscribeFromSymbol(this.props.ticker);
        this._subscriptions.forEach(subscription =>
            subscription.unsubscribe());
    }

    private _onLiveData(data: ISymbol) {
        if (data.symbol !== this.props.ticker) {
            // data for someone else, ignore it
            return;
        }

        let { loadingRealtime, cachedRealtimeData, cachedHistoricalData, chartData } = this.state;
        const { loadingHistorical } = this.state;

        if (loadingRealtime) {
            loadingRealtime = false;

            if (Env.DEBUG) {
                console.log('LiveChart::_onLiveData - toggling loading realtime data to false');
            }

            if (!loadingHistorical) {
                if (Env.DEBUG) {
                    console.log('LiveChart::_onLiveData - detected historical data already loaded, building chart data and flushing both caches');
                }

                chartData = []
                    .concat(chartData)
                    .concat(cachedHistoricalData)
                    .concat(cachedRealtimeData);
                cachedHistoricalData = [];
                cachedRealtimeData = [];
            }
        }

        if (loadingHistorical) {
            if (Env.DEBUG) {
                console.log('LiveChart::_onLiveData - detected historical data still loading, caching realtime data');
            }
            cachedRealtimeData = [].concat(cachedRealtimeData).concat(data);
        } else {
            chartData = [].concat(chartData).concat(data);
        }

        this.setState(prev => ({
            ...prev,
            loadingRealtime: loadingRealtime,
            cachedHistoricalData: cachedHistoricalData,
            cachedRealtimeData: cachedRealtimeData,
            chartData: this.expireData(chartData).sort(SortDescending)
        }));
    }

    private _onHistoricalData(data: IHistoricalIntradaySymbol[]) {
        if (data && data.length > 0) {
            let { loadingHistorical, cachedRealtimeData, cachedHistoricalData, chartData } = this.state;
            const { loadingRealtime } = this.state;

            if (loadingHistorical) {
                loadingHistorical = false;

                if (Env.DEBUG) {
                    console.log('LiveChart::_onLiveData - toggling loading historical data to false');
                }

                if (!loadingRealtime || !this._stocks.connected) {
                    if (Env.DEBUG) {
                        if (!loadingRealtime) {
                            console.log('LiveChart::_onLiveData - detected realtime data already streaming in, building chart data and flushing both caches');
                        }
                        if (!this._stocks.connected) {
                            console.log('LiveChart::_onLiveData - realtime connection not connected, build chart data and flush cache');
                        }
                    }
                    chartData = []
                        .concat(chartData)
                        .concat(cachedHistoricalData)
                        .concat(data)
                        .concat(cachedRealtimeData)
                    cachedHistoricalData = [];
                    cachedRealtimeData = [];
                }
            }

            if (loadingRealtime) {
                if (Env.DEBUG) {
                    console.log('LiveChart::_onLiveData - detected realtime data still loading, caching historical data');
                }
                cachedHistoricalData = [].concat(cachedHistoricalData).concat(data);
            }

            if (Env.DEBUG) {
                console.log('LiveChart::_onLiveData - emitting the following state update:', {
                    loadingHistorical, cachedHistoricalData, cachedRealtimeData, chartData
                });
            }

            this.setState(prev => ({
                ...prev,
                loadingHistorical: loadingHistorical,
                cachedHistoricalData: cachedHistoricalData,
                cachedRealtimeData: cachedRealtimeData,
                chartData: this.expireData(chartData).sort(SortDescending)
            }));
        } else {
            console.log(`LiveChart::_onHistoricalData - warning! historical intraday for ${this.props.ticker} empty`);
            this.setState(prev => ({
                ...prev,
                loadingHistorical: false
            }));
        }
    }

    private expireData(data: ISymbol[]): ISymbol[] {
        const { start, end } = this.state;

        // remove data older than the set chart start date,
        // and if an end date is defined, data that's newer
        // than the end date
        return data.filter(datum =>
            datum.date >= start &&
                (!end ||  datum.date <= end));
    }

    render() {
        if (this.loading) {
            return <BigLoader />
        }

        if (this.state.chartData.length > 0) {
            return <StaticChart
                chart={this.state.activeChartType}
                dimensions={{
                    width: 1200,
                    height: 600,
                    margin: {
                        top: 20,
                        bottom: 30,
                        left: 40,
                        right: 30
                    }
                } as IChartDimensions}
                data={this.state.chartData}
                />
        }

        return <div>No data found (live or historical!)</div>;
    }
};

export default LiveChart;
