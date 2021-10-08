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

import Account from "../../../models/Account";
import AccountRepository from "../../../repositories/AccountRepository";
import AccountIcon from "../../shared/Icons/AccountIcon";

export interface IAccountItemProps {
    account: Account;
}

export interface IAccountState {
}

class AccountItem extends React.Component<IAccountItemProps, IAccountState> {

    public get id(): number {
        return this.props.account.id;
    }

    public get accountName(): string {
        return this.props.account.name;
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

    private _accountRepo: AccountRepository;

    constructor(props: IAccountItemProps) {
        super(props);

        this.state = {};

        this.requestSync = this.requestSync.bind(this);

        this._accountRepo = new AccountRepository();
    }

    private formatDate(date: Date) {
        return moment(date).fromNow();
    }

    private async requestSync(accountId: number) {
        await this._accountRepo.refreshAccounts(accountId);
    }

    render() {
        return <div key={this.id}>
            <div className={styles.AccountItem}>
                <span className={styles.AccountItemIcon}>
                    <AccountIcon account={this.props.account} />
                </span>
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
