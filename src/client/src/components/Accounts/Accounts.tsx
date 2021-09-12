import Styles from "./Accounts.module.scss";
import React from "react";
import Header from "../Plaid/Headers";
import {QuickstartProvider} from "../Context";
import PlaidApp from "../Plaid/PlaidApp";
import Account from "../../models/Account";
import AccountRepository from "../../repositories/AccountRepository";
import AccountItem from "./AccountItem";
import {CashCoin} from "react-bootstrap-icons";
import PlaidRepository from "../../repositories/PlaidRepository";
import OpenLink from "../Plaid/OpenLink";
import {linkTo} from "@storybook/addon-links";
import Env from "../../env";

export interface IAccountProps {

}

export interface IAccountState {
    token: string;
    openPlaidLink: boolean;
    accounts: Account[];
}

class Accounts extends React.Component<IAccountProps, IAccountState> {

    private accountRepository: AccountRepository;
    private plaidRepository: PlaidRepository;

    constructor(props: IAccountProps) {
        super(props);

        this.state = {
            token: '',
            openPlaidLink: false,
            accounts: []
        };

        this._onAccountListUpdated = this._onAccountListUpdated.bind(this);
        this._onRequestLinkAccount = this._onRequestLinkAccount.bind(this);

        this.accountRepository = new AccountRepository();
        this.plaidRepository = new PlaidRepository();
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

    private async _onRequestLinkAccount() {
        let token = localStorage.getItem('link_token');
        if (!token) {
            if (Env.DEBUG) {
                console.log('Accounts::_onRequestLinkAccount - no token found in local storage, requesting one from server');
            }
            const response = await this.plaidRepository.createLinkToken();
            if (response.success) {
                token = response.data.link_token;
                // set the link token for plaid link to use later - this should either be done in plaidlink
                // or somewhere not here i think
                localStorage.setItem("link_token", response.data.link_token); //to use later for Oauth
            }
        } else if (Env.DEBUG) {
            console.log('Accounts::_onRequestLinkAccount - token found in local storage, re-using')
        }
        this.setState(prev => ({
            ...prev,
            token: token,
            openPlaidLink: true
        }));
    }

    renderAccounts() {
        return this.state.accounts.length > 0
            ? <div>
            {
                this.state.accounts.map(account => {
                    return <AccountItem account={account}></AccountItem>
                })
            }
        </div>
            : <div>
                <button onClick={this._onRequestLinkAccount}>
                    <CashCoin></CashCoin>
                    Link account
                </button>
            </div>
    }

    render() {
        return <div className={Styles.Accounts}>
            { this.renderAccounts() }
            { this.state.openPlaidLink && <OpenLink token={this.state.token} /> }
        </div>
    }
}

export default Accounts;
