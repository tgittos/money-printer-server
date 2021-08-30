import React from 'react';
import { Route, Redirect } from 'react-router-dom';
import AppStore from './../../AppStore';

export const PrivateRoute = ({ component: Component, ...rest }: any) => (
    <Route {...rest} render={props => {
        if (!AppStore.getState().profile?.authenticated) {
            return <Redirect to={{ pathname: '/login' }} />
        }
        // authorised so return component
        return <Component {...props} />
    }} />
)

export default PrivateRoute;
