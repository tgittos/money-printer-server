import {createSlice} from "@reduxjs/toolkit";
import {balanceReducers, createBalanceThunks, IBalanceState} from "../reducers/BalanceReducers";

const BalanceSlice = createSlice({
    name: 'balance',
    initialState: {
        idle: true,
        loading: false,
        balances: []
    } as IBalanceState,
    reducers: balanceReducers,
    extraReducers: createBalanceThunks
});

export default BalanceSlice;
