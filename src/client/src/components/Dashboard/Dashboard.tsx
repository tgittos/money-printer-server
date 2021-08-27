import React from 'react';
import styles from './Dashboard.module.scss';
import BigLoader from "../shared/Loaders/BigLoader";
import Header from "../Header/Header";

type DashboardProps = {
}

type DashboardState = {
}

class Dashboard extends React.Component<DashboardProps, DashboardState> {

    constructor(props: DashboardProps) {
        super(props);

        this.state = {
        } as DashboardProps;
    }

    render() {
        return <div className={styles.Dashboard}>
            <Header></Header>
            <BigLoader></BigLoader>
        </div>
    }
};

export default Dashboard;
