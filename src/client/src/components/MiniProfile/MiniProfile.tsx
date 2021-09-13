import React, {ChangeEvent} from 'react';
import styles from './MiniProfile.module.scss';

import I18nRepository from "../../repositories/I18nRepository";
import Profile, {IProfile} from "../../models/Profile";
import ProfileRepository from "../../repositories/ProfileRepository";
import {Modal, NavDropdown } from "react-bootstrap";
import Profiles from "../Profiles/Profiles";
import Env from "../../env";
import {Person, PersonCircle} from "react-bootstrap-icons";

interface MiniProfileProps {
    profile: IProfile;
    authenticated: boolean;
};
interface MiniProfileState {
    profile: IProfile;
    authenticated: boolean;
    showProfileModal: boolean;
    username: string;
    password: string;
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
            authenticated: props.authenticated,
            showProfileModal: false
        } as MiniProfileState;

        this.handleLogin = this.handleLogin.bind(this);
        this.handleLogout = this.handleLogout.bind(this);
        this.handleProfileModalShow = this.handleProfileModalShow.bind(this);
        this.handleProfileModalHide = this.handleProfileModalHide.bind(this);
        this.handleLoginFormChange = this.handleLoginFormChange.bind(this);

        this._profileRepository = new ProfileRepository();
        this._i18nRepository = new I18nRepository();
    }

    private async handleLogin() {
        const response = await this._profileRepository.auth({
            username: this.state.username,
            password: this.state.password
        });
        if (response.success) {
            const authedProfile = new Profile(response.data.profile);
            this.setState(prev => ({
                ...prev,
                profile: authedProfile,
                authenticated: true
            }));
        }
    }

    private handleLogout() {
        if (Env.DEBUG) {
            console.log('MiniProfile::handleLogout - performing logout');
        }
        this._profileRepository.logout()
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

    public renderAuthenticated() {
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
        </div>
    }

    private handleLoginFormChange(prop: string, ev: ChangeEvent<HTMLInputElement>) {
        this.setState(prev => ({
            ...prev,
            [prop]: ev.target.value
        }));
        ev.preventDefault();
    }

    public renderUnauthenticated() {
        return <div className={styles.MiniLogin}>
            <input name="miniProfileUsername" placeholder="Username"
                   onChange={(e) => this.handleLoginFormChange('username', e)}
                    />
            <input name="miniProfilePassword" placeholder="Password"
                   type="password"
                   onChange={(e) => this.handleLoginFormChange('password', e)}
                   />
            <button onClick={this.handleLogin}>Login</button>
        </div>
    }

    render() {
        const dropdownTitle = (<PersonCircle></PersonCircle>);
        return <NavDropdown title={dropdownTitle} id="profile-dropdown" className={styles.navItem}>

            { this.props.authenticated
                ? this.renderAuthenticated()
                : this.renderUnauthenticated() }

            <Modal dialogClassName={styles.MiniLoginProfileModal} show={this.showProfileModal} onHide={this.handleProfileModalHide}>
                <Modal.Header closeButton>
                    <Modal.Title>Profile</Modal.Title>
                </Modal.Header>
                <Modal.Body>
                    <Profiles profile={this.state.profile}></Profiles>
                </Modal.Body>
            </Modal>

        </NavDropdown>
    }
}

export default MiniProfile;
