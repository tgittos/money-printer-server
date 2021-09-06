import React from 'react';
import styles from './Dashboard.module.scss';
import Header from "../Header/Header";
import { IProfile } from "../../models/Profile";
import ClientHubRepository, { NullableSymbol } from "../../repositories/ClientHubRepository";
import {filter, Subscription} from "rxjs";
import SymbolTracker from "../SymbolTracker/SymbolTracker";
import Symbol, {ISymbol} from "../../models/Symbol";
import ZoomableChart from "../Charts/MultiLineChart/ZoomableChart";

import testData from '../../testData.csv';
import * as d3 from 'd3';
import BigLoader from "../shared/Loaders/BigLoader";
import Chart from "../Charts/Chart";
import CandleChart from "../Charts/lib/charts/CandleChart";
import IChartDimensions from "../Charts/interfaces/IChartDimensions";

interface IDashboardProps {
    profile: IProfile
}

interface IDashboardState {
    profile: IProfile,
    chartData: Symbol[];
}

const loadTestData = (async () => {
        const data = await d3.csv(testData);
        return data;
    });

class Dashboard extends React.Component<IDashboardProps, IDashboardState> {

    private _clientHub: ClientHubRepository;

    private _subscriptions: Subscription[] = [];

    constructor(props: IDashboardProps) {
        super(props);

        this.state = {
            profile: props.profile,
            chartData: []
        } as IDashboardState;

        this._onQuoteData = this._onQuoteData.bind(this)

        this._clientHub = new ClientHubRepository();

        // TEST JUNK
        loadTestData().then(data => this.setState(prev => ({
            ...prev,
            chartData: data
        })));
    }

    componentDidMount() {
        this._subscriptions.push(
            this._clientHub.liveQuotes$
                .pipe(
                    filter(val => !!val)
                )
                .subscribe(this._onQuoteData)
        );
    }

    componentWillUnmount() {
        this._subscriptions.forEach(subscription =>
            subscription.unsubscribe());
    }

    private _onQuoteData(data: ISymbol) {
        console.log('got data:', data);
        const { chartData } = this.state;
        this.setState(prev => ({
            ...prev,
            chartData: [].concat(chartData).concat(data as Symbol)
        }));
    }

    render() {
        if (this.state.chartData.length == 0) {
            return <BigLoader></BigLoader>
        }

        return <div className={styles.Dashboard}>
            <Header profile={this.state.profile}></Header>
            <SymbolTracker />
            <Chart
                chart={CandleChart}
                data={this.state.chartData}
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
            ></Chart>
        </div>
    }
};

export default Dashboard;
