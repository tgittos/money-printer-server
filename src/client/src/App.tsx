import './App.scss';
import React, {useContext} from "react";
import {Col, Container, Row} from "react-bootstrap";
import {Route, BrowserRouter as Router, Switch, useHistory} from "react-router-dom";

import Header from "./components/Header/Header";
import MainNav from "./components/MainNav/MainNav";
import {IAppState} from "./slices/AppSlice";

class App extends React.Component<{}, {}> {
  readonly cssClasses: string[] = [
      'mp', 'app'
  ];

  private get getState(): IAppState {
    return useContext(s:  => s:)
  }

  componentDidMount() {
  }

  componentWillUnmount() {
  }

  private _onNavigate(eventKey: string) {
    const history = useHistory();
    history.push("/" + eventKey);
  }

  render() {
    return <Container className={this.cssClasses.join(' ')}>
        <Row>
          <Col>
            <MainNav onNavigate={this._onNavigate} />
          </Col>
          <Col>
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
                  </Route>
                  <Route path="/accounts">
                  </Route>
                </Switch>
              </div>
            </Router>
          </Col>
        </Row>
    </Container>;
  }
}

export default App;
