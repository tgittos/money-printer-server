import React from "react";
import Account from "../../../models/Account";
import styles from "../Accounts.module.scss";
import AccountIcon from "../../shared/Icons/AccountIcon";
import {formatAsCurrency} from "../../../utilities";
import moment from "moment";
import Panel from "../../shared/Panel/Panel";

export interface IAccountTileProps {
    account: Account;
    className?: string;
}

class AccountTile extends React.Component<IAccountTileProps, {}> {
    render() {
        let s = [styles.AccountTile, 'mp-account-tile'];
        if (this.props.className) s = s.concat(Array.of(this.props.className));
        return <Panel className={s.join(' ')}>
            <div className="mp-chart small">
                Performance chart here
            </div>
            <p className="mp-chart-id">
                <AccountIcon account={this.props.account} />
                { this.props.account.name }
            </p>
            <p className="mp-chart-balance">
                { formatAsCurrency(this.props.account.balance) }
            </p>
            <ul className="mp-chart-performance">
                <li className="thirty">30d:</li>
                <li className="sixty">60d:</li>
                <li className="ninety">90d:</li>
            </ul>
            <p className="timestamp">
                { moment.utc(this.props.account.timestamp).fromNow() }
            </p>
        </Panel>;
    }
}

export default AccountTile;