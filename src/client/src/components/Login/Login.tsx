import React, {ChangeEvent} from 'react';
import styles from './Login.module.scss';

import ProfileRepository from '../../repositories/ProfileRepository';
import I18nRepository from './../../repositories/I18nRepository';
import IAuthProfileRequest from './../../requests/AuthProfileRequest';
import IAuthProfileResponse from "../../responses/AuthProfileResponse";
import ErrorList from "../shared/ErrorList/ErrorList";
import ErrorMessage from "../shared/ErrorMessage/ErrorMessage";

type LoginProps = {};
type LoginState = {
    username: string;
    password: string;
    errors: string[];
};

class Login extends React.Component<LoginProps, LoginState> {

    private _profileRepository: ProfileRepository;
    private _i18nRepository: I18nRepository;

    constructor(props: LoginProps) {
        super(props);

        this.state = {
            username: '',
            password: ''
        } as LoginState;

        this.handleLogin = this.handleLogin.bind(this);
        this.handleFieldChange = this.handleFieldChange.bind(this);

        this._profileRepository = new ProfileRepository();
        this._i18nRepository = new I18nRepository();
    }

    private async handleLogin() {
        const { username, password } = this.state;

        const response: IAuthProfileResponse = await this._profileRepository.auth({
            username: username,
            password: password
        } as IAuthProfileRequest);

        if (!response.success) {
            this.setState((prev, props) => ({
                ...prev,
                errors: [response.message]
            }));
        } else {
            this.setState((prev, props) => ({
                ...prev,
                errors: []
            }));
        }
    }

    private handleFieldChange(key: string, e: ChangeEvent<HTMLInputElement>)
    {
        this.setState((prev, props) => ({
            ...prev,
            [key]: e.target.value
        }))
    }

    private renderErrors() {
        if (this.state.errors && this.state.errors.length > 0) {
            return <ErrorMessage message={this.state.errors[0]} inline={false}></ErrorMessage>
        }
    }

    render() {
        return (
            <div className={styles.Login}>
                <div className={styles.LoginForm}>
                    { this.renderErrors() }
                    <p>
                        <label htmlFor="login_username">Username:</label>
                        <input id="login_username"
                               onChange={(e) => this.handleFieldChange("username", e)}
                               value={this.state.username}
                               placeholder={this._i18nRepository.t('login_username_placeholder')}></input>
                    </p>
                    <p>
                        <label htmlFor="login_password">Password:</label>
                        <input id="login_password"
                               onChange={(e) => this.handleFieldChange("password", e)}
                               type="password"
                               value={this.state.password}
                               placeholder={this._i18nRepository.t('login_password_placeholder')}></input>
                    </p>
                    <div className={styles.LoginFormFooter}>
                        <button
                            onClick={this.handleLogin}
                        >{this._i18nRepository.t('login_submit')}</button>
                    </div>
                </div>
            </div>
        );
    }
}

export default Login;
