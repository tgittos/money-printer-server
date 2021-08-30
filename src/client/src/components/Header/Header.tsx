import React from 'react';
import styles from './Header.module.scss';
import {Container, Nav, Navbar, NavDropdown} from "react-bootstrap";
import MiniLogin from "../Login/MiniLogin";
import Profile from "../../models/Profile";
import ProfileRepository from "../../repositories/ProfileRepository";
import {Subscription} from "rxjs";

type HeaderProps = {
}

type HeaderState = {
    currentProfile?: Profile
}

class Header extends React.Component<HeaderProps, HeaderState> {

    private _profileRepo: ProfileRepository;
    private _subscriptions: Subscription[] = [];

    constructor(props: HeaderProps) {
        super(props);

        this.state = {
            currentProfile: null
        } as HeaderProps;

        this._profileRepo = new ProfileRepository();
    }

    componentDidMount() {
        this._subscriptions.push(
        )
    }

    componentWillUnmount() {
        this._subscriptions.forEach(sub => sub.unsubscribe());
    }

    private onProfileUpdated(profile: Profile | null) {
        this.setState({
            currentProfile: profile
        } as HeaderProps)
    }

    getDropdownLabel() {
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
