import styles from './Register.module.scss';

import React, {ChangeEvent} from 'react';
import PropTypes from 'prop-types';
import {Observable, Subject, Subscription} from "rxjs";

import I18nRepository from '../../repositories/I18nRepository'
import ProfileRepository from '../../repositories/ProfileRepository'
import IRegisterProfileRequest from '../../requests/RegisterProfileRequest';
import IRegisterProfileResponse from '../../responses/RegisterProfileResponse';
import Profile from '../../models/Profile';

type RegisterProps = {
    onRegistration: (profile?: Profile | null) => void;
}

type RegisterState = {
    email: string;
    firstName: string;
    lastName: string;
    errors: string[];
}

class Register extends React.Component<RegisterProps, RegisterState> {

    private _registrationSubject: Subject<Profile> = new Subject<Profile>();
    private _publishRegistration = (profile: Profile) =>
        this._registrationSubject.next(profile);
    private _registrationSubscribers: Subscription[] = [];

    private _i18n: I18nRepository;
    private _profile: ProfileRepository;

    public get onRegistration(): Subject<Profile>
    {
        return this._registrationSubject;
    }

    constructor(props: RegisterProps) {
        super(props);

        // initialize state
        this.state = {
            email: '',
            firstName: '',
            lastName: ''
        } as RegisterState;

        // re-bind internal handlers
        this.handleSubmit = this.handleSubmit.bind(this);
        this.onEmailChanged = this.onEmailChanged.bind(this);
        this.onFirstNameChanged = this.onFirstNameChanged.bind(this);
        this.onLastNameChanged = this.onLastNameChanged.bind(this);

        // bind parent subscribers
        const { onRegistration } = this.props;
        this._registrationSubscribers.push(this._registrationSubject.subscribe(onRegistration));

        // initialize repositories
        this._i18n = new I18nRepository();
        this._profile = new ProfileRepository();
    }

    componentWillUnmount() {
        this._registrationSubscribers.forEach(sub => sub.unsubscribe());
    }

    public async handleSubmit(event: Event) {
        const { email, firstName, lastName } = this.state;

        console.log('this.state:', this.state);

        if (!this._validateRegistration()) {
            console.log('validation error');
            return false;
        }

        console.log('doing register');
        const response: IRegisterProfileResponse = await this._profile.register({
            email, firstName, lastName
        } as IRegisterProfileRequest);

        if (response.success) {
            this._publishRegistration(response.data);
        }

        event.preventDefault();
    }

    private _validateRegistration(): boolean {
        const errors: string[] = [];

        if (this.state.email === '') {
            errors.push(this._i18n.t("register_error_email_blank"));
        }

        if (this.state.firstName === '') {
            errors.push(this._i18n.t("register_error_first_name_blank"));
        }

        if (this.state.lastName === '') {
            errors.push(this._i18n.t("register_error_last_name_blank"));
        }

        this.setState(prevState => {
            prevState.errors = errors;
            return prevState;
        });

        return errors.length == 0;
    }

    public onEmailChanged(event: ChangeEvent) {
        this.setState(prevState => {
            prevState.email = event.target.value;
            return prevState;
        });
    }

    public onFirstNameChanged(event: ChangeEvent) {
        this.setState(prevState => {
            prevState.firstName = event.target.value;
            return prevState;
        });
    }

    public onLastNameChanged(event: ChangeEvent) {
        this.setState(prevState => {
            prevState.lastName = event.target.value;
            return prevState;
        });
    }

    renderErrors() {
        const { errors } = this.state;

        if (errors?.length > 0)
        {
            return <div className="errors">
                {errors.join('\n')}
            </div>
        }
    }

    render() {
        return <div className={styles.Register}>
            <div>
                <label>Email:</label>
                <input placeholder={this._i18n.t('register_email_placeholder')}
                       onChange={this.onEmailChanged}
                    value={this.state.email}></input>

                <label>First Name:</label>
                <input placeholder={this._i18n.t('register_first_name_placeholder')}
                       onChange={this.onFirstNameChanged}
                    value={this.state.firstName}></input>

                <label>Last Name:</label>
                <input placeholder={this._i18n.t('register_last_name_placeholder')}
                       onChange={this.onLastNameChanged}
                    value={this.state.lastName}></input>

                {this.renderErrors()}

                <button onClick={this.handleSubmit}>{this._i18n.t('register_submit')}</button>
            </div>
            <div>
                <p>{this._i18n.t('register_login', { href: '/profile/login'})}</p>
            </div>
        </div>
    }
}

export default Register;
