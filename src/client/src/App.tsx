import './App.scss';

import React from "react";

import AppStore, {getAccountsState, getAppState, getHoldingsState, getProfileState} from './stores/AppStore';
import { IAppState } from "./slices/AppSlice";
import I18nService from "./repositories/I18nRepository";
import ProfileRepository from "./repositories/ProfileRepository";
import Dashboard from "./components/Dashboard/Dashboard.lazy";
import BigLoader from "./components/shared/Loaders/BigLoader";
import AccountRepository from "./repositories/AccountRepository";
import Account, {IAccount} from "./models/Account";
import {Route, BrowserRouter as Router, Switch} from "react-router-dom";
import Header from "./components/Header/Header";
import Investments from "./components/Investments/Investments.lazy";
import Forecasting from "./components/Forecasting/Forecasting";

class App extends React.Component<{}, IAppState> {

  private _i18n: I18nService;
  private _profileRepo: ProfileRepository;
  private _accountRepo: AccountRepository;

  public get loading(): boolean {
    const profileState = getProfileState();
    const accountState = getAccountsState();
    return profileState.loading || (profileState.authenticated && accountState.loading);
  }

  constructor(props: {}) {
    super(props);

    this.state = getAppState();

    // load in all our stores and sync the current data state from the server
    this._i18n = new I18nService();
    this._profileRepo = new ProfileRepository();
    this._accountRepo = new AccountRepository();

    // subscribe to any realtime data sources we need to keep everything realtime

    AppStore.subscribe(() => {
      const newState = getAppState();
      this.setState(prev => ({
        ...prev,
        ...newState
      }));
    });
  }

  componentDidMount() {
    this._profileRepo.init();
    this._accountRepo.listAccounts();
  }

  componentWillUnmount() {
  }

  private filterInvestmentAccounts(accountShapes: IAccount[]): Account[] {
    return accountShapes.map(shape => new Account(shape))
        .filter(account => account.isInvestment);
  }

  render() {
    const profileState = getProfileState();
    const accountState = getAccountsState();

    if (this.loading) {
      return <div className="App">
        <BigLoader></BigLoader>
      </div>
    }

    if (!this.state.initialized) {
      return <div className="App">
        <div className="content">
          <div id="unconfigured">
            <img src="/loaders/nyan.gif" width="350" height="350" alt="nyan!" />
            <p>Uh oh! It looks like your install of Money Printer hasn't been initialized!</p>
            <p>Pop over to your server, and run <span className="code">bin/init</span> command to set 'er up.</p>
            <p>You'll be printing money in no time.</p>
          </div>;
        </div>
      </div>
    }

    // TODO convert router output components to lazy loaded ones
    return <div className="App">
        <Router>
          <div className="content">
            <Header profile={profileState.current} authenticated={profileState.authenticated} />
            <Switch>
              <Route path="/" exact>
                <Dashboard profile={profileState.current}
                           authenticated={profileState.authenticated}
                           accounts={accountState.accounts.map(account => new Account(account))}
                           balances={accountState.balances}
                />
              </Route>
              <Route path="/investments">
                <Investments accounts={this.filterInvestmentAccounts(accountState.accounts)} />
              </Route>
              <Route path="/forecasting">
                <Forecasting />
              </Route>
            </Switch>
          </div>
        </Router>
      </div>;
  }
}

export default App;
