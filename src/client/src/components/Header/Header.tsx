import React from 'react';
import styles from './Header.module.scss';
import {Container, Nav, Navbar, NavDropdown} from "react-bootstrap";
import MiniLogin from "../Login/MiniLogin";
import Profile from "../../models/Profile";
import AppStore from '../../AppStore';
import Env from "../../env";

type HeaderProps = {
}

type HeaderState = {
}

class Header extends React.Component<HeaderProps, HeaderState> {

    public get authenticated(): boolean {
        return AppStore.getState()?.profile?.authenticated;
    }

    public get currentProfile(): Profile | null {
        return AppStore.getState()?.profile?.current;
    }

    constructor(props: HeaderProps) {
        super(props);

        this.state = {
            currentProfile: null
        } as HeaderProps;

        this.getDropdownLabel = this.getDropdownLabel.bind(this);
    }

    componentDidMount() {
    }

    componentWillUnmount() {
    }

    getDropdownLabel() {
        if (Env.DEBUG) {
            console.log('Header::getDropdownLabel - authenticated?', this.authenticated);
            console.log('Header::getDropdownLabel - currentProfile:', this.currentProfile);
        }
        if (this.authenticated) {
            return "Logged in as: " + this.currentProfile?.firstName;
        }
        return "Login";
    }

    render() {
        const cssClassName = [
            styles.Header, "justify-content-end"
        ].join(' ');

        return <Navbar bg="dark" variant="dark" expand="lg">
            <Container>
                <Navbar.Brand href="#dashboard">
                    <img src="/logo192.png"
                         width="30" height="30"
                         className="d-inline-block align-top"
                         alt="logo" />{' '}
                    Money Printer
                </Navbar.Brand>
                <Nav className={cssClassName}>
                    <Nav.Link href="#dashboard">Dashboard</Nav.Link>
                    <Nav.Link href="#forecasting">Forecasting</Nav.Link>
                    <NavDropdown title={this.getDropdownLabel()} id="profile-dropdown" className={styles.navItem}>
                        <MiniLogin></MiniLogin>
                    </NavDropdown>
                </Nav>
            </Container>
        </Navbar>
    }
};

export default Header;
