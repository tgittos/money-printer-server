import {createSlice, PayloadAction} from "@reduxjs/toolkit";
import IAccount from "../interfaces/IAccount";
import {Pay} from "plaid";

export interface IAccountState {
    accounts: IAccount[];
}

const AccountSlice = createSlice({
    name: 'Account',
    initialState: {
        accounts: []
    } as IAccountState,
    reducers: {
        setAccounts(state: IAccountState, action: PayloadAction<IAccount[]>) {
            return {
                ...state,
                accounts: action.payload
            }
        },
        addAccount(state: IAccountState, action: PayloadAction<IAccount>) {
            return {
                ...state,
                accounts: [].concat(state.accounts).concat([action.payload])
            }
        }
    }
});

export const {
    setAccounts,
    addAccount,
} = AccountSlice.actions;
export default AccountSlice.reducer;
