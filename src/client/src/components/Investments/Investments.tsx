import styles from "./Investments.module.scss";
import React, {useState} from "react";
import {IAccountHolding} from "../../slices/AccountSlice";
import HoldingsList from "./HoldingsList/HoldingsList";
import Account from "../../models/Account";
import {getAccountsState} from "../../stores/AppStore";
import {Tab, Tabs} from "react-bootstrap";
import InvestmentAccountSummary from "./InvestmentAccountSummary/InvestmentAccountSummary";

export interface IInvestmentsProps {
    accounts: Account[];
}

export interface IInvestmentsState {
    tabState: { active: string; };
}

class Investments extends React.Component<IInvestmentsProps, IInvestmentsState> {

    constructor(props: IInvestmentsProps) {
        super(props);


        this.state = {
            tabState: { active: '' }
        };

        this.getAccount = this.getAccount.bind(this);
        this._onTabSelect = this._onTabSelect.bind(this);
    }

    componentDidMount() {
        const { tabState } = this.state;
        const firstAccountId = this.props.accounts[0]?.id;
        if (firstAccountId && tabState.active === '') {
            this.setState(prev => ({
               ...prev,
               tabState: {
                   ...tabState,
                   active: firstAccountId.toString()
               }
            }));
        }
    }

    public getAccount(accountId: number): Account {
        const { accounts } = this.props;
        const account = accounts.find(a => a.id == accountId);
        if (account !== undefined) {
            return account;
        }
        return null;
    }

    private get activeKey(): string {
        return this.state.tabState.active;
    }

    private _onTabSelect(key: string) {
        this.setState(prev => ({
            ...prev,
            tabState: {
                ...prev.tabState,
                active: key
            }
        }));
    }

    render() {
        return <div className={styles.Investments}>
            <Tabs activeKey={this.activeKey} onSelect={this._onTabSelect} className={styles.InvestmentTabs}>
                { this.props.accounts.map(account =>
                    <Tab key={account.id} title={account.name} eventKey={account.id} className={styles.InvestmentTabContent}>
                        <InvestmentAccountSummary account={account}></InvestmentAccountSummary>
                    </Tab>) }
            </Tabs>
        </div>
    }
}

export default Investments;
