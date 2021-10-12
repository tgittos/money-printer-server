import React from 'react';
import styles from './Header.module.scss';
import {Container, Nav, Navbar, NavDropdown} from "react-bootstrap";
import Profile, {IProfile} from "../../models/Profile";

type HeaderProps = {
    profile?: IProfile,
    authenticated?: boolean
}

type HeaderState = {
}

class Header extends React.Component<HeaderProps, HeaderState> {

    constructor(props: HeaderProps) {
        super(props);

        this.state = {
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

        return <Navbar variant="dark">
            <Container>
                <Navbar.Brand href="#dashboard">
                    <img src="/logo192.png"
                         width="30" height="30"
                         className="d-inline-block align-top"
                         alt="logo" />{' '}
                    Money Printer
                </Navbar.Brand>
            </Container>
        </Navbar>
    }
};

export default Header;
