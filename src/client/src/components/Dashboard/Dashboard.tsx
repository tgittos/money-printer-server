import React from 'react';
import styles from './Dashboard.module.scss';
import BigLoader from "../shared/Loaders/BigLoader";
import Header from "../Header/Header";
import { IProfile } from "../../models/Profile";
import MultiLineChart from "../Charts/MultiLineChart/MultiLineChart";
import ClientHubRepository, { NullableSymbol } from "../../repositories/ClientHubRepository";
import Env from "../../env";
import {Observable, Subscription} from "rxjs";
import {ListGroup} from "react-bootstrap";
import SymbolTracker from "../SymbolTracker/SymbolTracker";

interface IDashboardProps {
    profile: IProfile
}

interface IDashboardState {
    profile: IProfile,
}

class Dashboard extends React.Component<IDashboardProps, IDashboardState> {

    constructor(props: IDashboardProps) {
        super(props);


        this.state = {
            profile: props.profile,
        } as IDashboardState;
    }

    componentDidMount() {
    }

    componentWillUnmount() {
    }

    render() {
        return <div className={styles.Dashboard}>
            <Header profile={this.state.profile}></Header>
            <SymbolTracker />
            <MultiLineChart></MultiLineChart>
        </div>
    }
};

export default Dashboard;
