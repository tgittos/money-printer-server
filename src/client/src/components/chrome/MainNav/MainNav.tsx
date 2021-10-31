import React from "react";
import {Nav, Navbar} from "react-bootstrap";
import {useRecoilState} from "recoil";
import {appState} from "../../../App";
import {useHistory} from "react-router-dom";
import MainNavItem from "./components/MainNavItem";

export interface IMainNavProps {
    onNavigate: (e: string) => void;
    showAdmin?: boolean;
}

const MainNav = (props: IMainNavProps) => {
    let cssClasses: string[] = [
        'mp-main-nav',
        'flex-column'
    ];

    const history = useHistory();

    const routeAndSetApp = (key: string) => {
        history.push("/" + key);
        props.onNavigate(key);
    }

    return <div className="mp-nav-bg">
        <Navbar.Brand href="/">Money Printer</Navbar.Brand>
        <Nav className={cssClasses.join(' ')} onSelect={routeAndSetApp}>
            <Nav.Link eventKey="market">
                <MainNavItem>Market</MainNavItem>
            </Nav.Link>
            <Nav.Link eventKey="analysis">
                <MainNavItem>Analysis</MainNavItem>
            </Nav.Link>
            <Nav.Link eventKey="projection">
                <MainNavItem>Projection</MainNavItem>
            </Nav.Link>
            <Nav.Link eventKey="algo">
                <MainNavItem>Algo</MainNavItem>
            </Nav.Link>
            <br />
            <Nav.Link eventKey="profile">
                <MainNavItem>Profile</MainNavItem>
            </Nav.Link>
            <Nav.Link eventKey="accounts">
                <MainNavItem>Accounts</MainNavItem>
            </Nav.Link>
            { (props.showAdmin ?? false) &&
                <Nav.Link eventKey="admin">
                  <MainNavItem>Admin</MainNavItem>
                </Nav.Link>
            }
        </Nav>
    </div>
}

export default MainNav;
