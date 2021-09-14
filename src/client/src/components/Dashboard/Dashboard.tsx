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
import AccountPerformance from "../AccountPerformance/AccountPerformance";

interface IDashboardProps {
    profile: IProfile;
    accounts: Account[];
    authenticated: boolean;
}

interface IDashboardState {
}

class Dashboard extends React.Component<IDashboardProps, IDashboardState> {

    constructor(props: IDashboardProps) {
        super(props);

        this.state = {
        } as IDashboardState;
    }

    componentDidMount() {
    }

    componentWillUnmount() {
    }

    render() {
        return <div className={styles.Dashboard}>
            <Header profile={this.props.profile} authenticated={this.props.authenticated}></Header>
            <Overview accounts={this.props.accounts}></Overview>
            <AccountPerformance accounts={this.props.accounts}></AccountPerformance>
        </div>
    }
};

export default Dashboard;
