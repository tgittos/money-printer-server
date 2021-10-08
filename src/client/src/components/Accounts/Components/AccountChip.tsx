import styles from "../Accounts.module.scss";
import React from "react";
import Account from "../../../models/Account";
import AccountIcon from "../../shared/Icons/AccountIcon";
import {formatAsCurrency} from "../../../utilities";
import moment from "moment";
import Panel from "../../shared/Panel/Panel";
import StaticChart from "../../Charts/StaticChart";
import SparklineChart from "../../Charts/lib/charts/SparklineChart";
import {IBalance} from "../../../models/Balance";
import {formatBalancesForLine} from "../../../lib/ChartData";

export interface IAccountChipProps {
    account: Account;
    balanceHistory?: IBalance[];
    className?: string;
}

class AccountChip extends React.Component<IAccountChipProps, {}> {

    private get returnClass(): string {
        return this.props.account.balance > 0
            ? this.props.account.balance === 0
                ? ""
                : "gain"
            : "loss";
    }

    private get cssType(): string { return this.props.account.type.replace(' ', '-') + '-bg'; }
    private get cssSubtype(): string {
        return this.props.account.type.replace(' ', '-') + '-' +
            this.props.account.subtype.replace(' ', '-') + '-bg';
    }

    render() {
        let s = [styles.AccountChip, 'mp-account-chip', this.cssType, this.cssSubtype];
        if (this.props.className) s = s.concat(Array.of(this.props.className));
        return <Panel className={s.join(' ')}>
            <div className={[styles.AccountChipId].join(' ')}>
                <div className={styles.AccountChipIdTitle}>
                    { this.props.account.name }
                </div>
                <div className={["balance", this.returnClass].join(' ')}>{ formatAsCurrency(this.props.account.balance) }</div>
                <div className="timestamp">
                    <span>{ moment.utc(this.props.account.timestamp).fromNow() }</span>
                </div>
            </div>
            { this.props.balanceHistory && <div className={styles.AccountChipSparkline}>
                <StaticChart chart={SparklineChart}
                             dimensions={{
                                margin: {
                                    left: 0,
                                    right: 0,
                                    top: 0,
                                    bottom: 0
                                }
                             }}
                             data={formatBalancesForLine(this.props.balanceHistory)} />
            </div> }
        </Panel>;
    }
}

export default AccountChip;