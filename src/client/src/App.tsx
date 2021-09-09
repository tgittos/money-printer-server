import 'bootstrap/dist/css/bootstrap.min.css';
import './App.scss';

import React from "react";
import {
  BrowserRouter as Router,
  Switch,
  Route,
} from "react-router-dom";
import {io, Socket} from 'socket.io-client';

import AppStore from './AppStore';
import { IAppState } from "./slices/AppSlice";

import I18nRepository from "./repositories/I18nRepository";
import ProfileRepository from "./repositories/ProfileRepository";

import Profile from "./models/Profile";
import Dashboard from "./components/Dashboard/Dashboard";
import PrivateRoute from "./components/shared/PrivateRoute";
import Login from "./components/Login/Login";
import BigLoader from "./components/shared/Loaders/BigLoader";

interface IAppProps {

};

class App extends React.Component<IAppProps, IAppState> {

  private _i18n: I18nRepository;
  private _profileRepo: ProfileRepository;

  public get loading(): boolean {
    return AppStore.getState()?.profile?.loading === true;
  }

  public get currentProfile(): Profile | null {
    return AppStore.getState()?.profile?.current;
  }

  public get authenticated(): boolean {
    return AppStore.getState()?.profile.authenticated ?? false;
  }

  constructor(props: IAppProps) {
    super(props);

    this.state = {
    } as IAppState;

    this.onStateUpdated = this.onStateUpdated.bind(this);

    this._i18n = new I18nRepository();
    this._profileRepo = new ProfileRepository();

    this._profileRepo.init();
  }

  componentDidMount() {
    AppStore.subscribe(this.onStateUpdated);
  }

  componentWillUnmount() {
  }

  private onStateUpdated() {
    const newState = AppStore.getState();
    this.setState(newState);
  }

  render() {
    const unconfigured = <div id="unconfigured">
      <img src="/loaders/nyan.gif" width="350" height="350" alt="nyan!" />
      <p>Uh oh! It looks like your install of Money Printer hasn't been initialized!</p>
      <p>Pop over to your server, and run <span className="code">bin/init</span> command to set 'er up.</p>
      <p>You'll be printing money in no time.</p>
    </div>;

    if (this.loading) {
      return <div className="App">
        <BigLoader></BigLoader>
      </div>
    }

    if (this.currentProfile == null) {
      return <div className="App">
        <div className="content">
          {unconfigured}
        </div>
      </div>
    }


    return (
      <Router>
        <div className="App">
          <div className="content">
            <Switch>
              <PrivateRoute exact path="/">
                <Dashboard profile={this.currentProfile} />
              </PrivateRoute>
              <Route path="/login">
                <Login></Login>
              </Route>
            </Switch>
          </div>
        </div>
      </Router>);
  }
}

export default App;
