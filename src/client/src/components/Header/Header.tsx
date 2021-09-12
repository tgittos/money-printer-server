import React from 'react';
import styles from './Header.module.scss';
import {Container, Nav, Navbar, NavDropdown} from "react-bootstrap";
import MiniProfile from "../MiniProfile/MiniProfile";
import Profile, {IProfile} from "../../models/Profile";
import Env from "../../env";

type HeaderProps = {
    profile: IProfile,
    authenticated: boolean
}

type HeaderState = {
    profile: IProfile,
    authenticated: boolean
}

class Header extends React.Component<HeaderProps, HeaderState> {

    public get currentProfile(): Profile {
        return this.state.profile
    }

    constructor(props: HeaderProps) {
        super(props);

        this.state = {
            profile: props.profile,
            authenticated: props.authenticated
        } as HeaderProps;
    }

    componentDidMount() {
    }

    componentWillUnmount() {
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
                    <MiniProfile profile={this.state.profile} authenticated={this.state.authenticated}></MiniProfile>
               </Nav>
            </Container>
        </Navbar>
    }
};

export default Header;
