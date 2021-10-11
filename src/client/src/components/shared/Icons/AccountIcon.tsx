import styles from "./Icons.module.scss";
import Account from "../../../models/Account";
import React from "react";
import {Book, Calendar2Month, CashCoin, CashStack, CreditCard2Front, House, PiggyBank} from "react-bootstrap-icons";

export interface IAccountIconProps {
    className?: string;
    account: Account;
}

class AccountIcon extends React.Component<IAccountIconProps, {}> {

    private getIconForSubtype() {
        const { subtype } = this.props.account;
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
        let s = [styles.AccountIcon, 'mp-icon']
        if (this.props.className) s = s.concat(Array.of(this.props.className));
        return <div className={s.join(' ')}>
            { this.getIconForSubtype() }
        </div>;
    }
}

export default AccountIcon;