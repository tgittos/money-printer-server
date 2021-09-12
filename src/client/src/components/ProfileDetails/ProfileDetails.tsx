import Styles from './ProfileDetails.module.scss';
import React from "react";
import {IProfile} from "../../models/Profile";

export interface IProfileDetailsProps {
    profile: IProfile
}

export interface IProfileDetailsState {
    profile: IProfile
};

class ProfileDetails extends React.Component<IProfileDetailsProps, IProfileDetailsState> {

    constructor(props: IProfileDetailsProps) {
        super(props);

        this.state = {
            profile: this.props.profile
        };
    }

    render() {
        return <div className={Styles.ProfileDetails}>
            Profile details component
        </div>
    }
}

export default ProfileDetails;