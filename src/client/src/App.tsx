import './App.css';

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

  renderGreeting() {
    console.log('state:', this.state);
    if (this.state?.authenticated) {
      const currentProfile = this._profile.getCurrentProfile();
      return <p>Welcome, {currentProfile.firstName}</p>;
    }
    return <p>Please login or register to create a profile</p>;
  }

  render() {
    return (
      <Router>
        <div className="App">
        <div className="nav">
            <ul>
              <li>
                <Link to="/profile/register">Register</Link>
              </li>
            </ul>
        </div>
        <div className="content">
          <Switch>
            <Route path="/profile/register">
              <Register onRegistration={this.checkAuth} />
            </Route>
            <Route>
              {this.renderGreeting()}
            </Route>
          </Switch>
        </div>
      </div>
    </Router>
  );
  }
}

export default App;
