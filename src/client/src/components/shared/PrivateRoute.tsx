import React, {useContext} from 'react';
import { Route, Redirect } from 'react-router-dom';
import AppStore, {AppState} from './../../store/AppStore'
import Env from "../../env";
import {useAppSelector} from "../../store/AppHooks";
import {useRecoilValue} from "recoil";
import {ProfileContext} from "../../apps/profile/Profile.state";

export const PrivateRoute = ({ component: Component, ...rest }: any) => {

    const { state } = useContext(ProfileContext);

    const isAdmin = state.authenticated && !!state.current?.isAdmin;

    return <Route {...rest}>
        { !isAdmin && <Redirect to={{pathname: '/profile/login'}}/> }
        { isAdmin && <Component {...rest} /> }
    </Route>
};

export default PrivateRoute;
