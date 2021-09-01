import React from 'react';
import styles from './MiniLogin.module.scss';

import AppStore from '../../AppStore';

import I18nRepository from "../../repositories/I18nRepository";
import Profile from "../../models/Profile";
import {clearCurrentProfile} from "../../slices/ProfileSlice";

interface MiniLoginProps {

};
interface MiniLoginState {

};

class MiniLogin extends React.Component<MiniLoginProps, MiniLoginState> {

    private _i18nRepository: I18nRepository;

    public get authenticated(): boolean {
        return AppStore.getState()?.profile?.authenticated;
    }

    public get currentProfile(): Profile | null {
        return AppStore.getState()?.profile?.current;
    }

    constructor(props: MiniLoginProps) {
        super(props);

        this.state = {
        } as MiniLoginState;

        this.handleLogout = this.handleLogout.bind(this);

        this._i18nRepository = new I18nRepository();
    }

    private handleLogout() {
        console.log('clickin');
        AppStore.dispatch(clearCurrentProfile());
        return false;
    }

    renderAuthenticated() {
        return <div className={styles.MiniLogin}>
            <ul>
                <li>
                    My Profile
                </li>
                <li >
                    <button onClick={this.handleLogout}>
                        Logout
                    </button>
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
