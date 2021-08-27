import 'bootstrap/dist/css/bootstrap.min.css';
import './App.scss';

import React from "react";
import {
  BrowserRouter as Router,
  Switch,
  Route,
  Link
} from "react-router-dom";

import I18nRepository from "./repositories/I18nRepository";
import ProfileRepository from "./repositories/ProfileRepository";

import Profile from "./models/Profile";
import Dashboard from "./components/Dashboard/Dashboard";
import PrivateRoute from "./components/shared/PrivateRoute";
import Login from "./components/Login/Login";
import {skip, Subscription} from "rxjs";
import BigLoader from "./components/shared/Loaders/BigLoader";

type AppProps = {};
type AppState = {
  loading: boolean,
  currentProfile: Profile
};

class App extends React.Component<AppProps, AppState> {

  private _i18n: I18nRepository;
  private _profileRepo: ProfileRepository;

  private subscriptions: Subscription[] = [];

  public get loading(): boolean {
    return this.state.loading;
  }

  constructor(props: AppProps) {
    super(props);

    this.state = {
      loading: true
    } as AppProps;

    this._i18n = new I18nRepository();
    this._profileRepo = new ProfileRepository();
  }

  componentDidMount() {
    this.subscriptions.push(
        this._profileRepo.currentProfile$
            .pipe(skip(1))
            .subscribe(this.onProfileUpdated.bind(this))
    )
  }

  componentWillUnmount() {
    this.subscriptions.forEach(sub => sub.unsubscribe());
  }

  private onProfileUpdated(profile: Profile | null) {
    if (profile === null) {
      console.log('warn: no unauthenticated user established on server');
      this.setState((prev, props) => ({
        ...prev,
        loading: false
      }));
    } else {
      this.setState((prev, props) => ({
        ...prev,
        loading: false,
        currentProfile: profile
      }));
    }
  }

  render() {
    const unconfigured = <div id="unconfigured">
      <img src="/loaders/nyan.gif" width="350" height="350" alt="nyan!" />
      <p>Uh oh! It looks like your install of Money Printer hasn't been initialized!</p>
      <p>Pop over to your server, and run <span className="code">bin/init</span> command to set 'er up.</p>
      <p>You'll be printing money in no time.</p>
    </div>;

    if (this.state.loading)
    {
      return <div className="App">
        <BigLoader></BigLoader>
      </div>
    }

    if (this.state.currentProfile == null)
    {
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
              <PrivateRoute exact path="/" component={Dashboard} />
            </Switch>
          </div>
        </div>
      </Router>);
  }
}

export default App;
