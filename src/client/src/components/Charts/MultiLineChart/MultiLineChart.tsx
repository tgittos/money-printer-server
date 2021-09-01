import React from 'react';

import styles from './MultiLineChart.module.scss';
import {Container, Nav, Navbar, NavDropdown} from "react-bootstrap";

type MultiLineChartProps = {
}

type MultiLineChartState = {
    chartData: string | null;
}

class MultiLineChart extends React.Component<MultiLineChartProps, MultiLineChartState> {

    constructor(props: MultiLineChartState) {
        super(props);

        this.state = {
            chartData: null
        } as MultiLineChartState;
    }

    componentDidMount() {
        this.setState(prev => ({
            ...prev,
            chartData: this.generateChartData()
        }));
    }

    componentWillUnmount() {
    }

    private generateChartData(): string {
        return '';
    }

    render() {
        return <div className={styles.MultiLineChart}>
        </div>
    }
};

export default MultiLineChart;
