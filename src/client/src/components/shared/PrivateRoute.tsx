import React from 'react';
import { Route, Redirect } from 'react-router-dom';
import ProfileRepository from "../../repositories/ProfileRepository";

export const PrivateRoute = ({ component: Component, ...rest }: any) => (
    <Route {...rest} render={props => {
        const profileRepo = new ProfileRepository();
        const currentProfile = profileRepo.currentProfile;
        if (currentProfile == null) {
            return <Redirect to={{ pathname: '/login' }} />
        }
        // authorised so return component
        return <Component {...props} />
    }} />
)

export default PrivateRoute;
