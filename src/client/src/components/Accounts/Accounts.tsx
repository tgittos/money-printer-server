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
    accounts: Account[]
}

export interface IAccountState {
    token: string;
    openPlaidLink: boolean;
}

class Accounts extends React.Component<IAccountProps, IAccountState> {

    private plaidRepository: PlaidRepository;

    constructor(props: IAccountProps) {
        super(props);

        this.state = {
            token: '',
            openPlaidLink: false,
        };

        this._onRequestLinkAccount = this._onRequestLinkAccount.bind(this);

        this.plaidRepository = new PlaidRepository();
    }

    componentDidMount() {
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
        return this.props.accounts.length > 0
            ? <div>
            {
                this.props.accounts.map(account => {
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
