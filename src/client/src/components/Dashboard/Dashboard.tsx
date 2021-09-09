import React from 'react';
import styles from './Dashboard.module.scss';
import Header from "../Header/Header";
import { IProfile } from "../../models/Profile";
import SymbolTracker from "../SymbolTracker/SymbolTracker";

import BigLoader from "../shared/Loaders/BigLoader";
import LiveChart from "../Charts/LiveChart";

interface IDashboardProps {
    profile: IProfile
}

interface IDashboardState {
    profile: IProfile,
    loading: boolean,
}

class Dashboard extends React.Component<IDashboardProps, IDashboardState> {

    constructor(props: IDashboardProps) {
        super(props);

        this.state = {
            profile: props.profile,
            loading: false
        } as IDashboardState;
    }

    componentDidMount() {
    }

    componentWillUnmount() {
    }

    render() {
        if (this.state.loading) {
            return <BigLoader></BigLoader>
        }

        return <div className={styles.Dashboard}>
            <Header profile={this.state.profile}></Header>
            <SymbolTracker />
            <LiveChart></LiveChart>
        </div>
    }
};

export default Dashboard;
