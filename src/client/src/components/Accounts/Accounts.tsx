import Styles from "./Accounts.module.scss";
import React from "react";
import Header from "../Plaid/Headers";
import {QuickstartProvider} from "../Context";
import PlaidApp from "../Plaid/PlaidApp";
import Account from "../../models/Account";
import AccountRepository from "../../repositories/AccountRepository";
import AccountItem from "./AccountItem";

export interface IAccountProps {

}

export interface IAccountState {
    accounts: Account[];
}

class Accounts extends React.Component<IAccountProps, IAccountState> {

    private accountRepository: AccountRepository;

    constructor(props: IAccountProps) {
        super(props);

        this.state = {
            accounts: []
        };

        this._onAccountListUpdated = this._onAccountListUpdated.bind(this);

        this.accountRepository = new AccountRepository();
    }

    componentDidMount() {
        this.accountRepository.listAccounts().then(this._onAccountListUpdated);
    }

    private _onAccountListUpdated(accounts: Account[]) {
        if (accounts) {
            this.setState(prev => ({
                ...prev,
                accounts: accounts
            }));
        }
    }

    renderAccounts() {
        return <div>
            {
                this.state.accounts.map(account => {
                    return <AccountItem account={account}></AccountItem>
                })
            }
        </div>
    }

    render() {
        return <div className={Styles.Accounts}>
            <QuickstartProvider>
                <PlaidApp></PlaidApp>
            </QuickstartProvider>
            { this.renderAccounts() }
        </div>
    }
}

export default Accounts;
