import React from 'react';
import styles from './Dashboard.module.scss';
import Header from "../Header/Header";
import { IProfile } from "../../models/Profile";
import SymbolTracker from "../SymbolTracker/SymbolTracker";

import BigLoader from "../shared/Loaders/BigLoader";
import LiveChart from "../Charts/LiveChart";
import BasicLineChart from "../Charts/lib/charts/BasicLineChart";
import LiveQuoteRepository from "../../repositories/LiveQuoteRepository";
import {Subscription} from "rxjs";
import BasicCandleChart from "../Charts/lib/charts/BasicCandleChart";
import Overview from "../Overview/Overview";
import Account from "../../models/Account";

interface IDashboardProps {
    profile: IProfile;
    accounts: Account[];
    authenticated: boolean;
}

interface IDashboardState {
    chartedSymbols: string[];
}

class Dashboard extends React.Component<IDashboardProps, IDashboardState> {

    private _liveQuotes: LiveQuoteRepository;
    private _subscriptions: Subscription[] = [];

    constructor(props: IDashboardProps) {
        super(props);

        this.state = {
            chartedSymbols: []
        } as IDashboardState;

        this._onSubscribedSymbolsUpdated = this._onSubscribedSymbolsUpdated.bind(this);

        this._liveQuotes = LiveQuoteRepository.instance;
    }

    componentDidMount() {
        this._subscriptions.push(
            this._liveQuotes.subscribedSymbols$.subscribe(this._onSubscribedSymbolsUpdated)
        );
    }

    componentWillUnmount() {
        this._subscriptions.forEach(sub => sub.unsubscribe());
    }

    private _onSubscribedSymbolsUpdated(trackedSymbols: string[]) {
        this.setState(prev => ({
            ...prev,
            chartedSymbols: trackedSymbols
        }));
    }

    render() {
        const charts = this.state.chartedSymbols.map(ticker =>
            <LiveChart key={ticker} ticker={ticker} chart={BasicCandleChart}></LiveChart>
        );

        return <div className={styles.Dashboard}>
            <Header profile={this.props.profile} authenticated={this.props.authenticated}></Header>
            <Overview accounts={this.props.accounts}></Overview>
            <SymbolTracker disabled={!this.props.authenticated} />
            { charts }
        </div>
    }
};

export default Dashboard;
