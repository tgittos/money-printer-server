import React from 'react';
import styles from './MiniLogin.module.scss';

import IAuthProfileRequest from './../../requests/AuthProfileRequest';
import I18nRepository from "../../repositories/I18nRepository";
import ProfileRepository from "../../repositories/ProfileRepository";

type MiniLoginProps = {};
type MiniLoginState = {};

class MiniLogin extends React.Component<MiniLoginProps, MiniLoginState> {

    private _profileRepository: ProfileRepository;
    private _i18nRepository: I18nRepository;

    constructor(props: MiniLoginProps) {
        super(props);

        this.state = {
        } as MiniLoginState;

        this._profileRepository = new ProfileRepository();
        this._i18nRepository = new I18nRepository();
    }

    private auth(username: string, password: string) {
        const response = this._profileRepository.auth({
            username: username,
            password: password
        } as IAuthProfileRequest);
        console.log('response:', response);
    }

    render() {
        return <div className={styles.MiniLogin}>
            <input placeholder={this._i18nRepository.t('login_username_placeholder')}></input>
            <input placeholder={this._i18nRepository.t('login_password_placeholder')}></input>
            <button>{this._i18nRepository.t('login_submit')}</button>
        </div>
    }
}

export default MiniLogin;
