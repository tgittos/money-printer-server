import {IBalance} from "../../models/Balance";
import {PayloadAction} from "@reduxjs/toolkit";
import {IProfileState} from "./ProfileReducers";
import {GetBalanceHistoryForAccount} from "../thunks/BalanceThunks";

export interface IAccountBalance {
    accountId: number;
    balances: IBalance[];
}

export interface IBalanceState {
    idle: boolean;
    loading: boolean;
    error: string;
    balances: IAccountBalance[]
}

export const balanceReducers = {
    /*
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
     */
};


export const createBalanceThunks = ((builder: any) =>
        builder
            .addCase(GetBalanceHistoryForAccount.fulfilled, (state: IProfileState, action: PayloadAction<IBalance[]>) => {
                state.loading = false;
            })
            .addCase(GetBalanceHistoryForAccount.rejected, (state: IProfileState, action: string) => {
                state.error = action;
                state.loading = false;
            })
);

