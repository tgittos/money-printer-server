import React from 'react';
import styles from './Login.module.scss';

import ProfileRepository from '../../repositories/ProfileRepository';
import I18nRepository from './../../repositories/I18nRepository';
import IAuthProfileRequest from './../../requests/AuthProfileRequest';

type LoginProps = {};
type LoginState = {};

class Login extends React.Component<LoginState, LoginProps> {

    private _profileRepository: ProfileRepository;
    private _i18nRepository: I18nRepository;

    constructor(props: LoginProps) {
        super(props);

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
        return (
            <div className={styles.Login}>
                <div>
                    <form>
                        <label>Username:</label>
                        <input placeholder={this._i18nRepository.t('login_username_placeholder')}></input>

                        <label>Password:</label>
                        <input placeholder={this._i18nRepository.t('login_password_placeholder')}></input>

                        <button>{this._i18nRepository.t('login_submit')}</button>
                    </form>
                </div>
                <div>
                    <p>{this._i18nRepository.t('login_create_account', { href: '/profile/register'})}</p>
                </div>
            </div>
        );
    }
}

export default Login;
