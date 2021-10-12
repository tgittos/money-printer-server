import React from "react";
import {Nav} from "react-bootstrap";

export interface IMainNavProps {
    onNavigate: (e: string) => void;
}

class MainNav extends React.Component<IMainNavProps, {}> {
    readonly cssClasses: string[] = [
        'mp-main-nav',
        'flex-column'
    ];

    render() {
        return <Nav className={this.cssClasses.join(' ')}
                    onSelect={(key) => this.props.onNavigate(key)}>
            <Nav.Link eventKey="market">Market</Nav.Link>
            <Nav.Link eventKey="analysis">Analysis</Nav.Link>
            <Nav.Link eventKey="projection">Projection</Nav.Link>
            <Nav.Link eventKey="algo">Algo</Nav.Link>
            <br />
            <Nav.Link eventKey="profile">Profile</Nav.Link>
            <Nav.Link eventKey="accounts">Accounts</Nav.Link>
        </Nav>;
    }
}

export default MainNav;
