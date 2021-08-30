import 'bootstrap/dist/css/bootstrap.min.css';
import './App.scss';

import React from "react";
import {
  BrowserRouter as Router,
  Switch,
  Route,
  Link, Redirect
} from "react-router-dom";

import AppStore from './AppStore';
import { IAppState } from "./slices/AppSlice";

import I18nRepository from "./repositories/I18nRepository";
import ProfileRepository from "./repositories/ProfileRepository";

import Profile from "./models/Profile";
import Dashboard from "./components/Dashboard/Dashboard";
import PrivateRoute from "./components/shared/PrivateRoute";
import Login from "./components/Login/Login";
import {skip, Subscription} from "rxjs";
import BigLoader from "./components/shared/Loaders/BigLoader";

interface IAppProps {

};

class App extends React.Component<IAppProps, IAppState> {

  private _i18n: I18nRepository;
  private _profileRepo: ProfileRepository;

  private subscriptions: Subscription[] = [];

  public get loading(): boolean {
    return this.state?.profile?.loading === true;
  }

  public get currentProfile(): Profile | null {
    return this.state?.profile?.current ?? null;
  }

  public get authenticated(): boolean {
    return this.state?.profile.authenticated ?? false;
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
    console.log('unmounting');
    this.subscriptions.forEach(sub => sub.unsubscribe());
  }

  private onStateUpdated() {
    const newState = AppStore.getState();
    console.log('app state updated:', newState);
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
      console.log('detected loading');
      return <div className="App">
        <BigLoader></BigLoader>
      </div>
    }

    if (this.currentProfile == null) {
      console.log('detected unconfigured');
      return <div className="App">
        <div className="content">
          {unconfigured}
        </div>
      </div>
    }


    console.log('rendering login');

    return (
      <Router>
        <div className="App">
          <div className="content">
            <Switch>
              <Route path="/login">
                <Login></Login>
              </Route>
              <PrivateRoute exact path="/" component={Dashboard} />
            </Switch>
          </div>
        </div>
      </Router>);
  }
}

export default App;
