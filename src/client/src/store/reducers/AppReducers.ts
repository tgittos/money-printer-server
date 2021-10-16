import AuthService from "../../services/AuthService";
import {InitializeUnauthenticated} from "../thunks/ProfileThunks";
import {Initialize, SelectApp} from "../actions/AppActions";
import {SetCurrentProfile} from "../actions/ProfileActions";
import {Action, PayloadAction} from "@reduxjs/toolkit";
import {useHistory} from "react-router-dom";

const authService = new AuthService();

export interface IAppState {
    idle: boolean;
    loading: boolean;
    activeApp: string;
}

export const appReducers = {
    [SelectApp.type]: (state: IAppState, action: PayloadAction<string>) => {
        state.activeApp = action.payload
    },
    [Initialize.type]: (state: IAppState, action: Action) => {
        // all the server side bootstrapping gets triggered from here

        // bootstrap the app with either a previously authed user account
        // or initialize the application with the unauthenticated user state
        if (authService.currentProfile) {
            // dispatch(SetCurrentProfile(authService.currentProfile, true));
        } else {
            // dispatch(InitializeUnauthenticated());
        }
    },
};
