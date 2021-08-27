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

import Register from "./components/Register/Register";
import Profile from "./models/Profile";
import Header from "./components/Header/Header";
import BigLoader from "./components/shared/Loaders/BigLoader";

type AppProps = {};
type AppState = {
  authenticated: boolean
};

class App extends React.Component<AppProps, AppState> {

  private _i18n: I18nRepository;
  private _profile: ProfileRepository;

  constructor(props: AppProps) {
    super(props);

    this.setState({
      authenticated: false
    });

    this.checkAuth = this.checkAuth.bind(this);

    this._i18n = new I18nRepository();
    this._profile = new ProfileRepository();
  }

  componentDidMount() {
    this.checkAuth();
  }

  private checkAuth(profile: Profile | null = null) {
    const currentProfile = profile ?? this._profile.getCurrentProfile();
    this.setState({
      authenticated: currentProfile.authenticated
    } as AppState);
  }

  render() {
    return (
      <Router>
        <div className="App">
          <Header></Header>
          <div className="content">
            <Switch>
              <Route path="/profile/register">
                <Register onRegistration={this.checkAuth} />
              </Route>
              <Route>
                <BigLoader></BigLoader>
              </Route>
            </Switch>
          </div>
        </div>
      </Router>);
  }
}

export default App;
