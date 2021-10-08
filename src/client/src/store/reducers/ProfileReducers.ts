import {
    SetCurrentProfile,
    ClearCurrentProfile, IProfileActionArgs,
} from "../actions/ProfileActions";
import {PayloadAction} from "@reduxjs/toolkit";
import {useAppDispatch} from "../AppHooks";
import {ClearAccounts} from "../actions/AccountActions";
import {GetAccounts} from "../thunks/AccountThunks";
import {IAuthedProfile, IProfile} from "../../models/Profile";
import {AuthenticateUser, InitializeUnauthenticated} from "../thunks/ProfileThunks";
import AuthService from "../../services/AuthService";

const dispatch = useAppDispatch();
const auth = new AuthService();

export interface IProfileState {
    idle: boolean;
    loading: boolean;
    error: string;
    current: IProfile | null;

    authenticated: boolean;
    exp: Date;
}

export const profileReducers = {
    [SetCurrentProfile.type]: (state: IProfileState, action: PayloadAction<IProfileActionArgs>) => {
        state.current = action.payload.profile;
        state.authenticated = action.payload.authenticated;
        dispatch(GetAccounts());
    },
    [ClearCurrentProfile.type]: (state: IProfileState, action) => {
        state.current = null;
        state.authenticated = false;
        dispatch(ClearAccounts());
    }
};

export const createProfileThunks = (builder =>
    builder
        .addCase(InitializeUnauthenticated.fulfilled, (state: IProfileState, action: PayloadAction<IProfile>) => {
            dispatch(SetCurrentProfile(action.payload, false));
            state.loading = false;
        })
        .addCase(InitializeUnauthenticated.rejected, (state: IProfileState, action) => {
            state.error = action;
            state.loading = false;
        })
        .addCase(AuthenticateUser.fulfilled, (state: IProfileState, action: PayloadAction<IAuthedProfile>) => {
            state.error = '';
            auth.setToken(action.payload.token);
            dispatch(SetCurrentProfile(action.payload.profile, true));
            state.loading = false;
        })
        .addCase(AuthenticateUser.rejected, (state: IProfileState, action) => {
            state.error = action;
            state.loading = false;
            })
);

