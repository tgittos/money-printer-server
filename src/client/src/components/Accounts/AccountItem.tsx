import styles from './Accounts.module.scss';

import React from "react";
import {
    Book,
    Calendar2Month,
    CashCoin,
    CashStack,
    CreditCard2Front,
    House,
    PiggyBank
} from "react-bootstrap-icons";
import moment from "moment";

import Account from "../../models/Account";

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

    constructor(props: IAccountItemProps) {
        super(props);

        this.state = {};
    }

    private formatDate(date: Date) {
        return moment(date).fromNow();
    }

    private getIconForSubtype(subtype: string) {
        if (subtype === 'credit card') {
            return <CreditCard2Front></CreditCard2Front>
        }
        if (subtype === 'cd') {
            return <Calendar2Month></Calendar2Month>
        }
        if (subtype === "money market") {
            return <CashCoin></CashCoin>
        }
        if (subtype === "mortgage") {
            return <House></House>
        }
        if (["401k", "ira"].includes(subtype)) {
            return <PiggyBank></PiggyBank>
        }
        if (subtype === "student") {
            return <Book></Book>
        }
        return <CashStack></CashStack>
    }

    render() {
        return <div key={this.id}>
            <div className={styles.AccountItem}>
                <span className={styles.AccountItemIcon}>{ this.getIconForSubtype(this.subType) }</span>
                <span className={styles.AccountItemName}>{ this.accountName }</span>
                <span className={styles.AccountItemBalance}> { this.balance }</span>
                <span className={styles.AccountItemTimestamp}>last updated { this.formatDate(this.timestamp)}</span>
            </div>
        </div>
    }
}

export default AccountItem;
