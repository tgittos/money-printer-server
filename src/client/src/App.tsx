import 'bootstrap/dist/css/bootstrap.min.css';
import './App.scss';

import React from "react";
import {
  BrowserRouter as Router,
  Switch,
  Route,
} from "react-router-dom";

import AppStore, {getAccountsState, getAppState, getProfileState} from './stores/AppStore';
import { IAppState } from "./slices/AppSlice";

import I18nRepository from "./repositories/I18nRepository";
import ProfileRepository from "./repositories/ProfileRepository";

import Profile from "./models/Profile";
import Dashboard from "./components/Dashboard/Dashboard";
import PrivateRoute from "./components/shared/PrivateRoute";
import Login from "./components/Login/Login";
import BigLoader from "./components/shared/Loaders/BigLoader";
import AccountRepository from "./repositories/AccountRepository";

class App extends React.Component<{}, IAppState> {

  private _i18n: I18nRepository;
  private _profileRepo: ProfileRepository;
  private _accountRepo: AccountRepository;

  constructor(props: {}) {
    super(props);

    this.state = getAppState();

    this._i18n = new I18nRepository();
    this._profileRepo = new ProfileRepository();
    this._accountRepo = new AccountRepository();

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

  render() {
    const profileState = getProfileState();
    const accountState = getAccountsState();

    console.log('accountState:', accountState);

    if (this.state.loading) {
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

    return <div className="App">
          <div className="content">
            <Dashboard profile={profileState.current}
                       authenticated={profileState.authenticated}
                       accounts={accountState.accounts}
            />
          </div>
        </div>;
  }
}

export default App;
