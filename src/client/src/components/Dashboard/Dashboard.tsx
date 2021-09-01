import React from 'react';
import styles from './Dashboard.module.scss';
import BigLoader from "../shared/Loaders/BigLoader";
import Header from "../Header/Header";
import { IProfile } from "../../models/Profile";

type DashboardProps = {
    profile: IProfile
}

type DashboardState = {
    profile: IProfile
}

class Dashboard extends React.Component<DashboardProps, DashboardState> {

    constructor(props: DashboardProps) {
        super(props);

        this.state = {
            profile: props.profile
        } as DashboardProps;
    }

    render() {
        return <div className={styles.Dashboard}>
            <Header profile={this.state.profile}></Header>
            <BigLoader></BigLoader>
        </div>
    }
};

export default Dashboard;
