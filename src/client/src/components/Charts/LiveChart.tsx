import React from 'react';
import {filter, Subscription} from "rxjs";

import BigLoader from "../shared/Loaders/BigLoader";
import StaticChart from "../Charts/Chart";
import IChartDimensions from "../Charts/interfaces/IChartDimensions";
import LiveQuoteRepository from "../../repositories/LiveQuoteRepository";
import {IChartFactory} from "./lib/ChartFactory";
import HistoricalQuoteRepository from "../../repositories/HistoricalQuoteRepository";
import moment from 'moment';
import ISymbolResponse from "../../responses/SymbolsResponse";
import Env from "../../env";
import ISymbol from "../../interfaces/ISymbol";
import { SortDescending } from "../../interfaces/ISymbol";

interface ILiveChartProps {
    ticker: string;
    chart: IChartFactory;
    start?: Date;
    end?: Date;
}

interface ILiveChartState {
    loadingRealtime: boolean;
    loadingHistorical: boolean;
    cachedRealtimeData: ISymbol[];
    cachedHistoricalData: ISymbol[];
    chartData: ISymbol[];
    start: Date;
    end?: Date;
}

class LiveChart extends React.Component<ILiveChartProps, ILiveChartState> {

    private _liveQuotes: LiveQuoteRepository;
    private _historicalQuotes: HistoricalQuoteRepository;
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
            start: props.start ?? moment().subtract('days', 1);
        } as ILiveChartState;

        this._onLiveData = this._onLiveData.bind(this);
        this._onHistoricalData = this._onHistoricalData.bind(this);

        this._liveQuotes = LiveQuoteRepository.instance;
        this._historicalQuotes = new HistoricalQuoteRepository();
    }

    componentDidMount() {
        this._subscriptions.push(
            this._liveQuotes.connected$.subscribe(connected => {
                if (connected) {
                    if (Env.DEBUG) {
                        console.log('LiveChart::componentDidMount - connected to live quotes, subscribing to stream')
                    }
                    this._subscriptions.push(
                        this._liveQuotes.liveQuotes$
                            .pipe(filter(val => val !== undefined))
                            .subscribe(this._onLiveData)
                    );
                    const today: Date = new Date();
                    if (Env.DEBUG) {
                        console.log('LiveChart::componentDidMount - fetching historical data for ticker');
                    }
                    this._historicalQuotes.historicalIntraday(this.props.ticker, today)
                        .then(this._onHistoricalData);
                }
            })
        );
        this.setState(prev => ({
            ...prev,
            loading: false
        }))
    }

    componentWillUnmount() {
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

    private _onHistoricalData(response: ISymbolResponse) {
        if (response.success) {
            let { loadingHistorical, cachedRealtimeData, cachedHistoricalData, chartData } = this.state;
            const { loadingRealtime } = this.state;
            const { data } = response;

            if (loadingHistorical) {
                loadingHistorical = false;

                if (Env.DEBUG) {
                    console.log('LiveChart::_onLiveData - toggling loading historical data to false');
                }

                if (!loadingRealtime) {
                    if (Env.DEBUG) {
                        console.log('LiveChart::_onLiveData - detected realtime data already streaming in, building chart data and flushing both caches');
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
            console.log(`LiveChart::_onHistoricalData - warning! historical intraday for ${this.props.ticker} failed: ${response.message}`);
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
            return <BigLoader></BigLoader>
        }

        if (this.state.chartData.length > 0) {
            return <StaticChart
                chart={this.props.chart}
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
            ></StaticChart>
        }

        return <div>No data found (live or historical!)</div>;
    }
};

export default LiveChart;
