import React from 'react';
import styles from './Header.module.scss';
import {Col, Container, Nav, Navbar, NavDropdown, Row} from "react-bootstrap";
import Profile, {IProfile} from "../../../models/Profile";
import MarketTracker from "./components/MarketTracker";
import NotificationsBadge from "./components/NotificationsBadge";
import ProfileBadge from "./components/ProfileBadge";

export interface IHeaderProps {
    profile: IProfile;
}

const Header = (props: IHeaderProps) => {

    return <div className={styles.Header}>
        <Row>
            <Col>
                <MarketTracker />
            </Col>
            <Col sm="3">
                <ProfileBadge className="shift-right" profile={props.profile} />
                <NotificationsBadge className="shift-right" notificationCount={0} />
            </Col>
        </Row>
    </div>
};

export default Header;
