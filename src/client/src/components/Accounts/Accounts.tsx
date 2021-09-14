import styles from "./Accounts.module.scss";
import React, {ChangeEvent} from "react";
import Header from "../Plaid/Headers";
import {QuickstartProvider} from "../Context";
import PlaidApp from "../Plaid/PlaidApp";
import Account from "../../models/Account";
import AccountRepository from "../../repositories/AccountRepository";
import AccountItem from "./AccountItem";
import {CashCoin, Search} from "react-bootstrap-icons";
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
    filterState: IFilterState;
}

interface IFilterState {
    nameFilter: string;
    showAssets: boolean;
    showDebts: boolean;
}

class Accounts extends React.Component<IAccountProps, IAccountState> {

    private plaidRepository: PlaidRepository;

    constructor(props: IAccountProps) {
        super(props);

        this.state = {
            token: '',
            openPlaidLink: false,
            filterState: {
                nameFilter: '',
                showAssets: true,
                showDebts: true
            }
        };

        this._onRequestLinkAccount = this._onRequestLinkAccount.bind(this);
        this._onFiltersUpdated = this._onFiltersUpdated.bind(this);
        this._filterData = this._filterData.bind(this);

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

    private _onFiltersUpdated(propKey: string, ev: ChangeEvent<HTMLInputElement>) {
        const { filterState } = this.state;
        if (filterState.hasOwnProperty(propKey)) {
            if (ev.target.getAttribute('type') === 'checkbox') {
                filterState[propKey] = ev.target.checked;
            } else {
                filterState[propKey] = ev.target.value;
            }
        }
        this.setState(prev => ({
            ...prev,
            filterState
        }));
    }

    private _filterData(data: Account[]): Account[] {
        const { nameFilter, showAssets, showDebts } = this.state.filterState;

        let filteredData = [].concat(data);

        if (!showAssets) {
            filteredData = filteredData.filter(account =>
                !['depository', 'investment'].includes(account.type));
        }

        if (!showDebts) {
            filteredData = filteredData.filter(account =>
                !['credit', 'loan'].includes(account.type));
        }

        if (nameFilter && nameFilter !== '') {
            // apply the name filter to the data
            filteredData = filteredData.filter(account =>
                account.name.toLowerCase().includes(nameFilter.toLowerCase()));
        }

        console.log('filteredData:', filteredData);

        return filteredData;
    }

    renderAccounts() {
        const accountList = this.props.accounts.length > 0
            ? <div>
            {
                this._filterData(this.props.accounts).map(account => {
                    return <AccountItem account={account}></AccountItem>
                })
            }
        </div>
            : <></>

        return <>
                { accountList }
            </>
    }

    render() {
        return <div className={styles.Accounts}>
            <div className={styles.AccountsFilter}>
                <div>
                    <Search></Search>
                    <input name="accountNameFilter"
                           onChange={(ev) => this._onFiltersUpdated('nameFilter', ev)}
                           placeholder="Search..." />
                </div>
                <div>
                    <input type="checkbox"
                           checked={this.state.filterState.showAssets}
                           onChange={(ev) => this._onFiltersUpdated('showAssets', ev)} />
                    Show assets
                </div>
                <div>
                    <input type="checkbox"
                            checked={this.state.filterState.showDebts}
                           onChange={(ev) => this._onFiltersUpdated('showDebts', ev)} />
                    Show debts
                </div>
                <div className={styles.AccountsAddButtonContainer}>
                    <button onClick={this._onRequestLinkAccount}>
                        Link account
                    </button>
                </div>
            </div>
            { this.renderAccounts() }
            { this.state.openPlaidLink && <OpenLink token={this.state.token} /> }
        </div>
    }
}

export default Accounts;
