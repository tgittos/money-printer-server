import {createSlice, PayloadAction} from "@reduxjs/toolkit";
import IAccount from "../interfaces/IAccount";
import Account from "../models/Account";

export interface IAccountState {
    accounts: Account[];
}

const AccountSlice = createSlice({
    name: 'Account',
    initialState: {
        accounts: []
    } as IAccountState,
    reducers: {
        setAccounts(state: IAccountState, action: PayloadAction<Account[]>) {
            return {
                ...state,
                accounts: [].concat(action.payload)
            }
        },
        addAccount(state: IAccountState, action: PayloadAction<Account>) {
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
