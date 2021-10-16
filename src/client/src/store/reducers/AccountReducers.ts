import {Action, PayloadAction} from "@reduxjs/toolkit";
import {IAccount} from "../../models/Account";
import {GetAccounts, RefreshAccountDetails} from "../thunks/AccountThunks";
import {AddAccounts, ClearAccounts} from "../actions/AccountActions";
import {IHolding} from "../../models/Holding";
import {IProfileState} from "./ProfileReducers";

export interface IAccountHolding {
    accountId: number;
    holdings: IHolding[];
}

export interface IAccountState {
    idle: boolean;
    loading: boolean;
    error: string;
    accounts: IAccount[]
}

export const accountReducers = {
    [AddAccounts.type]: (state: IAccountState, action: PayloadAction<IAccount[]>) => {
        state.accounts = state.accounts.concat(action.payload);
        state.loading = false;
    },
    [ClearAccounts.type]: (state: IAccountState, action: Action) => {
        state.accounts = [];
    }
}

export const createAccountThunks = ((builder: any) =>
        builder
            .addCase(GetAccounts.fulfilled, (state: IProfileState, action: PayloadAction<IAccount[]>) => {
                // dispatch(AddAccounts(action.payload));
                state.loading = false;
            })
            .addCase(GetAccounts.rejected, (state: IProfileState, action: string) => {
                state.error = action;
                state.loading = false;
            })
            .addCase(RefreshAccountDetails.fulfilled, (state: IProfileState, action: PayloadAction<IAccount[]>) => {
                // dispatch(AddAccounts(action.payload));
                state.error = '';
                state.loading = false;
            })
            .addCase(RefreshAccountDetails.rejected, (state: IProfileState, action: string) => {
                state.error = action;
                state.loading = false;
            })
);

