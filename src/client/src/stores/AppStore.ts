import { configureStore } from '@reduxjs/toolkit';

import ProfileSlice, {IProfileState} from "./../slices/ProfileSlice";
import AppSlice, {IAppState} from "./../slices/AppSlice";
import PlaidSlice, {IPlaidState} from "../slices/PlaidSlice";

const appStore = configureStore({
    reducer: {
        app: AppSlice,
        profile: ProfileSlice,
        plaid: PlaidSlice
    }
});

export function getAppState(): IAppState {
    return (appStore.getState() as { app: IAppState }).app;
}

export function getProfileState(): IProfileState {
    return (appStore.getState() as { profile: IProfileState}).profile;
}

export function getPlaidState(): IPlaidState {
    return (appStore.getState() as { plaid: IPlaidState}).plaid;
}

export default appStore;
