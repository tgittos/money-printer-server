import React from 'react';
import styles from './Dashboard.module.scss';
import Header from "../Header/Header";
import { IProfile } from "../../models/Profile";
import Overview from "../Overview/Overview";
import Account from "../../models/Account";
import AccountPerformance from "../AccountPerformance/AccountPerformance";
import {IAccountBalance} from "../../slices/AccountSlice";

interface IDashboardProps {
    profile: IProfile;
    accounts: Account[];
    balances: IAccountBalance[];
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
            <Overview accounts={this.props.accounts}></Overview>
            <AccountPerformance accounts={this.props.accounts} balances={this.props.balances}></AccountPerformance>
        </div>
    }
};

export default Dashboard;
