import styles from './../Accounts.module.scss';

import React from "react";
import moment from "moment";
import Panel from "../../shared/Panel/Panel";
import StaticChart from "../../Charts/StaticChart";
import BasicLineChart from "../../Charts/lib/charts/BasicLineChart";
import {formatBalancesForLine} from "../../../lib/ChartData";
import Balance from "../../../models/Balance";
import {cssSubtype, cssType, returnClass} from "../AccountsHelper";
import Account from "../../../models/Account";
import {formatAsCurrency} from "../../../utilities";

export interface IAccountTileProps {
    account: Account;
    balanceHistory?: Balance[];
    className?: string;
}

interface IAccountTileState {
}

class AccountTile extends React.Component<IAccountTileProps, IAccountTileState> {

    public get id(): number {
        return this.props.account.id;
    }

    public get accountName(): string {
        return this.props.account.name;
    }

    public get type(): string {
        return this.props.account.type;
    }

    public get subType(): string {
        return this.props.account.subtype;
    }

    public get timestamp(): Date {
        return this.props.account.timestamp;
    }

    public get balance(): string {
        return this.props.account.formatBalanceAsCurrency();
    }

    constructor(props: IAccountTileProps) {
        super(props);

        this.state = {};

        this.requestSync = this.requestSync.bind(this);
    }

    private formatDate(date: Date) {
        return moment(date).fromNow();
    }

    private async requestSync(accountId: number) {
    }

    render() {
        let s = [styles.AccountTile, 'mp-account-tile', cssType(this.props.account), cssSubtype(this.props.account),
            returnClass(this.props.account)];
        if (this.props.className) s = s.concat(Array.of(this.props.className));
        return <Panel className={s.join(' ')}>
            <div className={styles.AccountTileIdentity}>
                <p className="name">
                    { this.props.account.name }
                </p>
                <p className="timestamp">
                    { moment.utc(this.props.account.timestamp).fromNow() }
                </p>
            </div>
            <div className={[styles.AccountTileBalance, 'balance'].join(' ')}>
                { formatAsCurrency(this.props.account.balance) }
            </div>
            { this.props.balanceHistory && <div className={styles.AccountTileChart}>
                <StaticChart chart={BasicLineChart}
                             dimensions={{
                                 margin: {
                                     top: 0,
                                     right: 0,
                                     bottom: 25,
                                     left: 45
                                 }
                             }}
                             data={formatBalancesForLine(this.props.balanceHistory)} />
            </div> }
            <ul className="mp-chart-performance">
                <li className="thirty">
                    <p className="return">foo</p>
                    <p className="label">30</p>
                </li>
                <li className="sixty">
                    <p className="return">foo</p>
                    <p className="label">60</p>
                </li>
                <li className="ninety">
                    <p className="return">foo</p>
                    <p className="label">90</p>
                </li>
            </ul>
        </Panel>;
    }
}

export default AccountTile;
