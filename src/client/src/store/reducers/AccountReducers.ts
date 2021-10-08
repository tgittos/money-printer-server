import {PayloadAction} from "@reduxjs/toolkit";
import {IAccount} from "../../models/Account";
import {GetAccounts, RefreshAccountDetails} from "../thunks/AccountThunks";
import {AddAccounts, ClearAccounts} from "../actions/AccountActions";
import {IBalance} from "../../models/Balance";
import {IHolding} from "../../models/Holding";
import {useAppDispatch} from "../AppHooks";
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

const dispatch = useAppDispatch();

export const accountReducers = {
    [AddAccounts.type]: (state: IAccountState, action: PayloadAction<IAccount[]>) => {
        state.accounts = state.accounts.concat(action.payload);
        state.loading = false;
    },
    [ClearAccounts.type]: (state: IAccountState, action) => {
        state.accounts = [];
    }
}

export const createAccountThunks = (builder =>
        builder
            .addCase(GetAccounts.fulfilled, (state: IProfileState, action: PayloadAction<IAccount[]>) => {
                dispatch(AddAccounts(action.payload));
                state.loading = false;
            })
            .addCase(GetAccounts.rejected, (state: IProfileState, action) => {
                state.error = action;
                state.loading = false;
            })
            .addCase(RefreshAccountDetails.fulfilled, (state: IProfileState, action: PayloadAction<IAccount[]>) => {
                dispatch(AddAccounts(action.payload));
                state.error = '';
                state.loading = false;
            })
            .addCase(RefreshAccountDetails.rejected, (state: IProfileState, action) => {
                state.error = action;
                state.loading = false;
            })
);

