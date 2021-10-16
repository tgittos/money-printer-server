import {GetHoldingsForAccount} from "../thunks/HoldingThunks";
import {IAccount} from "../../models/Account";
import {IHolding} from "../../models/Holding";
import {PayloadAction} from "@reduxjs/toolkit";

export interface IAccountHolding {
    account: IAccount;
    holdings: IHolding[];
}

export interface IHoldingState {
    idle: boolean;
    loading: boolean;
    error: string;
    holdings: IAccountHolding[];
}

export const holdingReducers = {
}

export const createHoldingThunks = ((builder: any) =>
    builder
        .addCase(GetHoldingsForAccount.fulfilled, (state: IHoldingState, action: PayloadAction<IHolding[]>) => {
            // figure out how to insert the holdings for this account into the map
            // where do we get the account ID from?
            state.loading = false;
        })
        .addCase(GetHoldingsForAccount.rejected, (state: IHoldingState, action: PayloadAction<string>) => {
            state.error = action.payload;
            state.loading = false;
        })
);