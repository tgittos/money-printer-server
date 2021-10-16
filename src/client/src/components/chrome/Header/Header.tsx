import React from 'react';
import styles from './Header.module.scss';
import {Container, Nav, Navbar, NavDropdown} from "react-bootstrap";
import Profile, {IProfile} from "../../../models/Profile";
import MarketTracker from "./components/MarketTracker";
import NotificationsBadge from "./components/NotificationsBadge";
import ProfileBadge from "./components/ProfileBadge";

export interface IHeaderProps {
    profile: IProfile;
}

const Header = (props: IHeaderProps) => {

    return <div className={styles.Header}>
        <MarketTracker />
        <ProfileBadge className="shift-right" profile={props.profile} />
        <NotificationsBadge className="shift-right" notificationCount={0} />
    </div>
};

export default Header;
