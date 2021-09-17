import { configureStore } from '@reduxjs/toolkit';

import ProfileSlice, {IProfileState} from "./../slices/ProfileSlice";
import AppSlice, {IAppState} from "./../slices/AppSlice";
import PlaidSlice, {IPlaidState} from "../slices/PlaidSlice";
import AccountSlice, {IAccountBalance, IAccountHolding, IAccountState} from "../slices/AccountSlice";

const appStore = configureStore({
    reducer: {
        app: AppSlice,
        profile: ProfileSlice,
        plaid: PlaidSlice,
        accounts: AccountSlice
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

export function getAccountsState(): IAccountState {
    return (appStore.getState() as { accounts: IAccountState }).accounts;
}

export function getHoldingsState(): IAccountHolding[] {
    return (appStore.getState() as { accounts: IAccountState }).accounts.holdings;
}

export function getBalancesState(): IAccountBalance[] {
    return (appStore.getState() as { accounts: IAccountState }).accounts.balances;
}

export default appStore;
