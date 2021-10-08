import {createSlice, PayloadAction} from "@reduxjs/toolkit";
import {accountReducers, createAccountThunks, IAccountState} from "../reducers/AccountReducers";

const AccountSlice = createSlice({
    name: 'accounts',
    initialState: {
        idle: true,
        loading: false,
        accounts: [],
    } as IAccountState,
    reducers: accountReducers,
    extraReducers: createAccountThunks
});

export default AccountSlice;
