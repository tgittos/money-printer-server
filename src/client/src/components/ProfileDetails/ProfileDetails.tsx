import Styles from './ProfileDetails.module.scss';
import React from "react";

export interface IProfileDetailsProps {

}

export interface IProfileDetailsState {

};

class ProfileDetails extends React.Component<IProfileDetailsProps, IProfileDetailsState> {
    render() {
        return <div className={Styles.ProfileDetails}>
            Profile details component
        </div>
    }
}

export default ProfileDetails;