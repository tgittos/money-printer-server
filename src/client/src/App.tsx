import './App.scss';
import React, {useContext, useState} from "react";
import {Col, Container, Row} from "react-bootstrap";
import {Route, BrowserRouter as Router, Switch, Link} from "react-router-dom";

import Header from "./components/chrome/Header/Header";
import MainNav from "./components/chrome/MainNav/MainNav";
import ProfileApp from "./apps/profile/Profile.lazy";
import {atom, RecoilRoot, useRecoilState, useRecoilValue, useSetRecoilState} from "recoil";
import ErrorBoundary from "./components/shared/ErrorBoundary/ErrorBoundary";
import PrivateRoute from "./components/shared/PrivateRoute";
import {ProfileContext} from "./apps/profile/Profile.state";

export const appState = atom({
  key: 'appState',
  default: 'dashboard'
});

const App = () => {
  const cssClasses: string[] = [
      'mp', 'app'
  ];

  const [navState, setNav] = useState("/");
  const profileState = { state } = useContext(ProfileContext);

  return <div className={cssClasses.join(' ')}>
        <Router>
          <Row className="mp-app-row">
          <Col md="auto" className="mp-nav-col">
            <MainNav onNavigate={setNav}
                     showAdmin={profileState.current?.isAdmin ?? false}
            />
          </Col>
          <Col className="mp-app-col">
            <Header profile={profileState?.current} />
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
                      <ProfileApp profile={profileState?.current} />
                    </Route>
                    <Route path="/accounts">
                    </Route>
                    <PrivateRoute path="/admin">
                    </PrivateRoute>
                  </Switch>
              </div>
          </Col>
        </Row>
    </Router>
</div>;
}

export default App;
