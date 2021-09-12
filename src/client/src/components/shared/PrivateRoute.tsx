import React from 'react';
import { Route, Redirect } from 'react-router-dom';
import AppStore, {getProfileState} from './../../stores/AppStore';
import Env from "../../env";

export const PrivateRoute = ({ component: Component, ...rest }: any) => (
    <Route {...rest} render={props => {
        const profileState = getProfileState();
        if (Env.DEBUG) {
            console.log('PrivateRoute - profileState:', profileState);
        }
        if (!profileState?.authenticated) {
            if (Env.DEBUG) {
                console.log('PrivateRoute - user not authenticated, redirecting to login');
            }
            return <Redirect to={{ pathname: '/login' }} />
        }
        // authorised so return component
        if (Env.DEBUG) {
            console.log('PrivateRoute - user authenticated, passing to requested uri');
        }
        console.log('props:', props);
        return <Component {...props} />
    }} />
)

export default PrivateRoute;
