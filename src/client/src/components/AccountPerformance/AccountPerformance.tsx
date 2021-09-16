import styles from "./AccountPerformance.module.scss";
import Account from "../../models/Account";
import Balance from "../../models/Balance";
import React from "react";
import AccountRepository from "../../repositories/AccountRepository";
import { Promise as BluebirdPromise } from "bluebird";
import Env from "../../env";
import MultiLineChart, {IMultiLineChartDataEntry} from "../Charts/lib/charts/MultiLineChart";
import IChartMargin from "../Charts/interfaces/IChartMargin";
import ILineDataPoint from "../Charts/interfaces/ILineDataPoint";
import StaticChart from "../Charts/StaticChart";
import {IAccountBalance} from "../../slices/AccountSlice";

export interface IAccountPerformanceProps {
    accounts: Account[]
    balances: IAccountBalance[]
}

export interface IAccountPerformanceState {
}

class AccountPerformance extends React.Component<IAccountPerformanceProps, IAccountPerformanceState> {

    constructor(props: IAccountPerformanceProps) {
        super(props);

        this.state = {
            chartAccounts: []
        };

        this._getData = this._getData.bind(this);
    }

    componentDidMount() {
    }

    private _getData(): IMultiLineChartDataEntry[] {
        const chartData = this.props.balances.map(accountBalance => {
            const account = this.props.accounts.find(account => account.id === accountBalance.accountId);
            const data = (accountBalance.balances ?? []).map(balance => {
                return {
                    x: balance.timestamp,
                    y: balance.current
                } as ILineDataPoint
            });

            return {
                name: account.name,
                data
            } as IMultiLineChartDataEntry;
        });
        return chartData;
    }

    render() {
        return <div className={styles.AccountPerformance}>
            <StaticChart
                chart={MultiLineChart}
                dimensions={{
                    width: 1200,
                    height: 600,
                    margin: {
                        top: 0,
                        left: 45,
                        right: 0,
                        bottom: 25
                    } as IChartMargin
                }}
                data={this._getData()} />
        </div>
    }
}

export default AccountPerformance
