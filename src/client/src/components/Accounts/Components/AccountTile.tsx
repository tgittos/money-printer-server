import styles from './../Accounts.module.scss';

import React from "react";
import {
    ArrowRepeat,
    Book,
    Calendar2Month,
    CashCoin,
    CashStack,
    CreditCard2Front,
    House,
    PiggyBank
} from "react-bootstrap-icons";
import moment from "moment";

import AppStore from "../../../stores/AppStore";
import Account from "../../../models/Account";

export interface IAccountTileProps {
    account: Account;
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
        AppStore.dispatch()
        await this._accountRepo.refreshAccounts(accountId);
    }

    render() {
        return <div key={this.id}>
            <div className={styles.AccountItem}>
                <span className={styles.AccountItemIcon}>{ this.getIconForSubtype(this.subType) }</span>
                <span className={styles.AccountItemName}>{ this.accountName }</span>
                <span className={styles.AccountItemBalance}> { this.balance }</span>
                <span className={styles.AccountItemTimestamp}>last updated { this.formatDate(this.timestamp)}</span>
                <span className={styles.AccountItemRefresh}>
                    <button onClick={() => this.requestSync(this.id)}>
                        <ArrowRepeat></ArrowRepeat>
                    </button>
                </span>
            </div>
        </div>
    }
}

export default AccountItem;
