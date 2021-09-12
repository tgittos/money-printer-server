import React from 'react';
import styles from './MiniProfile.module.scss';

import I18nRepository from "../../repositories/I18nRepository";
import Profile, {IProfile} from "../../models/Profile";
import ProfileRepository from "../../repositories/ProfileRepository";
import {Modal} from "react-bootstrap";
import Profiles from "../Profiles/Profiles";

interface MiniProfileProps {
    profile: IProfile
};
interface MiniProfileState {
    profile: IProfile,
    showProfileModal: boolean
};

class MiniProfile extends React.Component<MiniProfileProps, MiniProfileState> {

    private _profileRepository: ProfileRepository;
    private _i18nRepository: I18nRepository;

    public get currentProfile(): Profile {
        return this.state.profile
    }

    public get showProfileModal(): boolean {
        return this.state.showProfileModal;
    }

    constructor(props: MiniProfileProps) {
        super(props);

        this.state = {
            profile: props.profile,
            showProfileModal: false
        } as MiniProfileState;

        this.handleLogout = this.handleLogout.bind(this);
        this.handleProfileModalShow = this.handleProfileModalShow.bind(this);
        this.handleProfileModalHide = this.handleProfileModalHide.bind(this);

        this._profileRepository = new ProfileRepository();
        this._i18nRepository = new I18nRepository();
    }

    private handleLogout() {
        this._profileRepository.logout()
        return false;
    }

    private handleProfileModalShow() {
        this.setState(prev => ({
            ...prev,
            showProfileModal: true
        }));
    }

    private handleProfileModalHide() {
        this.setState(prev => ({
            ...prev,
            showProfileModal: false
        }));
    }

    render() {
        return <div className={styles.MiniLogin}>
            <ul>
                <li>
                    <button onClick={this.handleProfileModalShow}>
                        My Profile
                    </button>
                </li>
                <li>
                    <button onClick={this.handleLogout}>
                        Logout
                    </button>
                </li>
            </ul>

            <Modal show={this.showProfileModal} onHide={this.handleProfileModalHide}>
                <Modal.Header closeButton>
                    <Modal.Title>Profile</Modal.Title>
                </Modal.Header>
                <Modal.Body>
                    <Profiles></Profiles>
                </Modal.Body>
            </Modal>
        </div>
    }
}

export default MiniProfile;
