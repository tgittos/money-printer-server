import styles from "./AccountPerformance.module.scss";
import Account from "../../models/Account";
import Balance from "../../models/Balance";
import React from "react";
import AccountRepository from "../../repositories/AccountRepository";
import { Promise } from "bluebird";
import Env from "../../env";
import MultiLineChart, {IMultiLineChartDataEntry} from "../Charts/lib/charts/MultiLineChart";
import IChartMargin from "../Charts/interfaces/IChartMargin";
import ILineDataPoint from "../Charts/interfaces/ILineDataPoint";
import StaticChart from "../Charts/StaticChart";

export interface IAccountPerformanceProps {
    accounts: Account[]
}

export interface IAccountPerformanceState {
    chartAccounts: {
        account: Account | null,
        balances: Balance[]
    }[]
}

class AccountPerformance extends React.Component<IAccountPerformanceProps, IAccountPerformanceState> {

    private _accountRepo: AccountRepository;

    constructor(props: IAccountPerformanceProps) {
        super(props);

        this.state = {
            chartAccounts: []
        };

        this._onReceivedBalances = this._onReceivedBalances.bind(this);
        this._getData = this._getData.bind(this);

        this._accountRepo = new AccountRepository();
    }

    componentDidMount() {
        if (Env.DEBUG) {
            console.log("AccountPerformance::componentDidMount - querying accounts for balance history:", this.props.accounts);
        }
        Promise.all(
            this.props.accounts.map(account =>
                this._accountRepo.getBalances(account.id)))
            .then(this._onReceivedBalances);
    }

    private _onReceivedBalances(responses: Balance[][]) {
        const chartAccounts = responses.map(balances => {
            if (balances.length > 0) {
                const peek = balances[0];
                const account = this.props.accounts.filter(a => a.id == peek.accountId)[0];
                return {
                    account, balances
                }
            }
            return null;
        }).filter(chartAccount => !!chartAccount);

        if (chartAccounts != null && chartAccounts.length > 0) {
            if (Env.DEBUG) {
                console.log("AccountPerformance::_onReceivedBalances - got chart data, updating state")
            }
            this.setState(prev => ({
                ...prev,
                chartAccounts: chartAccounts
            }));
        }
    }

    private _getData(): IMultiLineChartDataEntry[] {
        const chartData = this.state.chartAccounts.map(account => {
            const data = account.balances.map(balance => {
                return {
                    x: balance.timestamp,
                    y: balance.current
                } as ILineDataPoint
            });

            return {
                name: account.account.name,
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
