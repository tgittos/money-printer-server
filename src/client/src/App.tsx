import './App.scss';
import React from "react";
import {Col, Container, Row} from "react-bootstrap";
import {Route, BrowserRouter as Router, Switch, useHistory} from "react-router-dom";

import Header from "./components/chrome/Header/Header";
import MainNav from "./components/chrome/MainNav/MainNav";
import {SelectApp} from "./store/actions/AppActions";
import ProfileApp from "./apps/profile/Profile.lazy";
import {connect} from "react-redux";
import Profile from "./models/Profile";

const mapState: any = (state: AppState) => {
  const { profile } = state;
  return {
    currentProfile: new Profile(profile.current)
  };
}
type AppState = ReturnType<typeof mapState>;

const mapDispatch: any = (dispatch: AppDispatch) => {
  return {
    selectApp: (e: string) => dispatch(SelectApp(e))
  }
};
type AppDispatch = ReturnType<typeof mapDispatch>;

type IAppProps = {} & AppState & AppDispatch;

class App extends React.Component {
  readonly cssClasses: string[] = [
      'mp', 'app'
  ];
  readonly props: IAppProps;

  constructor(props: IAppProps) {
    super(props);
    this.props = props;

    this._onNavigate = this._onNavigate.bind(this);
  }

  componentDidMount() {
  }

  componentWillUnmount() {
  }

  private _onNavigate(eventKey: string) {
    this.props.selectApp(eventKey);
  }

  render() {
    return <div className={this.cssClasses.join(' ')}>
        <Row className="mp-app-row">
          <Col xs="2" className="mp-nav-col">
            <MainNav onNavigate={this._onNavigate} />
          </Col>
          <Col className="mp-app-col">
            <Header />
            <Router>
              <div className="mp-app">
                <Switch>
                  <Route path="/" exact>
                  </Route>
                  <Route path="/market">
                  </Route>
                  <Route path="/analysis">
                  </Route>
                  <Route path="/projection">
                  </Route>
                  <Route path="/algo">
                  </Route>
                  <Route path="/profile">
                    <ProfileApp profile={this.props.currentProfile} />
                  </Route>
                  <Route path="/accounts">
                  </Route>
                </Switch>
              </div>
            </Router>
          </Col>
        </Row>
    </div>;
  }
}

export default connect(mapState, mapDispatch)(App);
