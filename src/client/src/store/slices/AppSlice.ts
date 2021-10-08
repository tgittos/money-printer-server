import {createSlice, PayloadAction} from "@reduxjs/toolkit";
import {appReducers} from "../reducers/AppReducers";

export interface IAppState {
    loading: boolean;
    initialized: boolean;
}

const AppSlice = createSlice({
    name: 'App',
    initialState: {
        loading: true,
        initialized: false
    } as IAppState,
    reducers: appReducers
});

export default AppSlice;
