import {createSlice, PayloadAction} from "@reduxjs/toolkit";
import IAccount from "../interfaces/IAccount";
import Account from "../models/Account";

export interface IAccountState {
    accounts: Account[];
}

// convert a given Account or Account[] to the appropriate
// IAccount or IAccount[] response
function accountToIAccount(data: Account | Account[]): IAccount  | IAccount[]{
    if (!(data as any).push) {
        data = [data as Account];
    }

    const iAccounts = (data as Account[]).map(account => ({
        id: account.id,
        name: account.name,
        type: account.type,
        subtype: account.subtype,
        balance: account.balance,
        timestamp: account.timestamp
    }) as IAccount);

    if (iAccounts.length == 1) {
        return iAccounts[0];
    }

    return iAccounts;
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
                accounts: [].concat(accountToIAccount(action.payload))
            }
        },
        addAccount(state: IAccountState, action: PayloadAction<Account>) {
            return {
                ...state,
                accounts: [].concat(state.accounts).concat(accountToIAccount([action.payload]))
            }
        }
    }
});

export const {
    setAccounts,
    addAccount,
} = AccountSlice.actions;
export default AccountSlice.reducer;
