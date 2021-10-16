import './App.scss';
import React from "react";
import {Col, Container, Row} from "react-bootstrap";
import {Route, BrowserRouter as Router, Switch, Link} from "react-router-dom";

import Header from "./components/chrome/Header/Header";
import MainNav from "./components/chrome/MainNav/MainNav";
import ProfileApp from "./apps/profile/Profile.lazy";
import {currentProfileState, profileState} from "./apps/profile/Profile";
import {atom, RecoilRoot, useRecoilState, useRecoilValue, useSetRecoilState} from "recoil";
import ErrorBoundary from "./components/shared/ErrorBoundary/ErrorBoundary";

export const appState = atom({
  key: 'appState',
  default: 'dashboard'
});

const App = () => {
  const cssClasses: string[] = [
      'mp', 'app'
  ];

  return <div className={cssClasses.join(' ')}>
        <Router>
          <Row className="mp-app-row">
          <Col md="auto" className="mp-nav-col">
            <MainNav onNavigate={useSetRecoilState(appState)} />
          </Col>
          <Col className="mp-app-col">
            <Header profile={useRecoilValue(currentProfileState)} />
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
                      <ProfileApp profile={useRecoilValue(currentProfileState)} />
                    </Route>
                    <Route path="/accounts">
                    </Route>
                  </Switch>
              </div>
          </Col>
        </Row>
    </Router>
</div>;
}

export default App;
