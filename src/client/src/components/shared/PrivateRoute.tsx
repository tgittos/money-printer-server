import React from 'react';
import { Route, Redirect } from 'react-router-dom';
import AppStore from './../../AppStore';
import Env from "../../env";

export const PrivateRoute = ({ component: Component, ...rest }: any) => (
    <Route {...rest} render={props => {
        const currentProfile = AppStore.getState().profile;
        if (currentProfile?.authenticated == true) {
            if (Env.DEBUG) {
                console.log('PrivateRoute - user not authenticated, redirecting to login');
            }
            return <Redirect to={{ pathname: '/login' }} />
        }
        // authorised so return component
        if (Env.DEBUG) {
            console.log('PrivateRoute - user authenticated, passing to requested uri');
        }
        return <Component {...props} />
    }} />
)

export default PrivateRoute;
