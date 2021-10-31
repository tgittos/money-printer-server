import styles from "../Header.module.scss";
import React from "react";
import {MdPerson} from "react-icons/all";
import Profile, {IProfile} from "../../../../models/Profile";
import {Dropdown} from "react-bootstrap";

export interface IProfileBadgeProps {
    className?: string;
    profile: IProfile;
    authenticated?: boolean;
}

interface IProfileBadgeButtonProps {
   name: string
}

const ProfileBadgeButton = (props: IProfileBadgeButtonProps) => {
    return <Dropdown.Toggle size="sm" variant="link">
        <span className="mp-avatar">
            <MdPerson />
        </span>
        <span className="mp-username">
            { props.name }
        </span>
    </Dropdown.Toggle>
}

const ProfileBadge = (props: IProfileBadgeProps) => {
    const classes = [
        props.className ?? '',
        styles.ProfileBadge,
        'mp-profile-badge',
    ]

    const profile = new Profile(props.profile);
    const authed = props.authenticated ?? false;

    return <Dropdown className={classes.join(' ')}>
        <ProfileBadgeButton name={profile.firstName} />
        <Dropdown.Menu>
            {authed ?
                <>
                    <Dropdown.Item href="/profile">Profile</Dropdown.Item>
                    <Dropdown.Item href="/profile/logout">Logout</Dropdown.Item>
                </>
                : <Dropdown.Item href="/profile/login" >Login</Dropdown.Item>
            }
        </Dropdown.Menu>
    </Dropdown>
}

export default ProfileBadge;
