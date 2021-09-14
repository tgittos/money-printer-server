import styles from "./Overview.module.scss";
import React from "react";
import Account from "../../models/Account";
import {formatAsCurrency} from "../../utilities";
import millify from "millify";

export interface IOverviewProps {
    accounts: Account[]
}

export interface IOverviewState {

}

class Overview extends React.Component<IOverviewProps, IOverviewState> {

    constructor(props: IOverviewProps) {
        super(props);

        this.state = {

        }
    }

    private calculateNetWorth() {
        return '$' + millify(
            this.props.accounts.reduce((prev, curr) => {
                return curr.isAsset
                    ? prev + curr.balance
                    : prev - curr.balance;
            }, 0));
    }

    private calculateDebts() {
        return '$' + millify(this.props.accounts.reduce((prev, curr) => {
            return curr.isDebt
                ? prev + curr.balance
                : prev;
            }, 0));
    }

    private calculateAssets() {
        return '$' + millify(this.props.accounts.reduce((prev, curr) => {
            return curr.isAsset
                ? prev + curr.balance
                : prev;
        }, 0))
    }

    private get thirtyDayReturns(): string {
        return "0%"
    }

    private get sixtyDayReturns(): string {
        return "0%"
    }

    private get ninetyDayReturns(): string {
        return "0%"
    }

    private get riskProfile(): string {
        return "moderate"
    }

    render() {
        console.log(this.props.accounts)
        return <div className={styles.Overview}>
            <div>Accounts<span className="statValue">{this.props.accounts.length}</span></div>
            <div>Net worth<span className="statValue">{this.calculateNetWorth()}</span></div>
            <div>Assets<span className="statValue">{this.calculateAssets()}</span></div>
            <div>Debts<span className="statValue">{this.calculateDebts()}</span></div>
            <div>30d<span className="statValue">{this.thirtyDayReturns}</span></div>
            <div>60d<span className="statValue">{this.sixtyDayReturns}</span></div>
            <div>90d<span className="statValue">{this.ninetyDayReturns}</span></div>
            <div>Risk<span className="statValue">{this.riskProfile}</span></div>
        </div>
    }
}

export default Overview
