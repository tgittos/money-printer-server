import React from 'react';
import Header from "../Header/Header";
import {filter, Subscription} from "rxjs";
import Symbol, {ISymbol} from "../../models/Symbol";

import BigLoader from "../shared/Loaders/BigLoader";
import Chart from "../Charts/Chart";
import IChartDimensions from "../Charts/interfaces/IChartDimensions";
import LiveQuoteRepository from "../../repositories/LiveQuoteRepository";
import BasicChart from "./lib/charts/BasicChart";
import Line from "./lib/figures/Line";
import BasicCandleChart from "./lib/charts/BasicCandleChart";

interface ILiveChartProps {
}

interface ILiveChartState {
    loading: boolean;
    chartData: Symbol[];
}

class LiveChart extends React.Component<ILiveChartProps, ILiveChartState> {

    private _liveQuotes: LiveQuoteRepository;
    private _subscriptions: Subscription[] = [];

    constructor(props: ILiveChartProps) {
        super(props);

        this.state = {
            loading: true,
            chartData: [],
        } as ILiveChartState;

        this._onQuoteData = this._onQuoteData.bind(this);

        this._liveQuotes = LiveQuoteRepository.instance;
    }

    componentDidMount() {
        this._subscriptions.push(
            this._liveQuotes.connected$.subscribe(connected => {
                if (connected) {
                    this._subscriptions.push(
                        this._liveQuotes.liveQuotes$
                            .pipe(filter(val => val !== undefined))
                            .subscribe(this._onQuoteData)
                    );
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

    private _onQuoteData(data: Symbol) {
        const { chartData } = this.state;
        this.setState(prev => ({
            ...prev,
            loading: false,
            chartData: [].concat(chartData)
                .concat(data as Symbol)
                .sort((s1, s2) => {
                    return s2.date < s1.date
                        ? -1
                        : s1.date < s2.date
                            ? 1
                            : 0;
                })
                .slice(0, 500)
        }));
    }

    render() {
        if (this.state.loading) {
            return <BigLoader></BigLoader>
        }

        if (this.state.chartData.length > 0) {
            return <Chart
                chart={BasicCandleChart}
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
            ></Chart>
        }

        return <div></div>;
    }
};

export default LiveChart;
