import React from 'react';
import styles from './MiniLogin.module.scss';

import AppStore from '../../AppStore';

import IAuthProfileRequest from './../../requests/AuthProfileRequest';
import I18nRepository from "../../repositories/I18nRepository";
import ProfileRepository from "../../repositories/ProfileRepository";
import Profile from "../../models/Profile";

interface MiniLoginProps {

};
interface MiniLoginState {

};

class MiniLogin extends React.Component<MiniLoginProps, MiniLoginState> {

    private _profileRepository: ProfileRepository;
    private _i18nRepository: I18nRepository;

    public get authenticated(): boolean {
        return AppStore.getState()?.profile?.authenticated;
    }

    public get currentProfile(): Profile {
        return AppStore.getState()?.profile?.current;
    }

    constructor(props: MiniLoginProps) {
        super(props);

        this.state = {
        } as MiniLoginState;

        this._profileRepository = new ProfileRepository();
        this._i18nRepository = new I18nRepository();
    }

    renderAuthenticated() {
        return <div className={styles.MiniLogin}>
            <ul>
                <li>
                    My Profile
                </li>
                <li>
                    Logout
                </li>
            </ul>
        </div>
    }

    renderUnauthenticated() {
        return <div className={styles.MiniLogin}>
            <input placeholder={this._i18nRepository.t('login_username_placeholder')}></input>
            <input placeholder={this._i18nRepository.t('login_password_placeholder')}></input>
            <button>{this._i18nRepository.t('login_submit')}</button>
        </div>
    }

    render() {
        if (this.authenticated) {
            return this.renderAuthenticated();
        }
        return this.renderUnauthenticated();
    }
}

export default MiniLogin;
