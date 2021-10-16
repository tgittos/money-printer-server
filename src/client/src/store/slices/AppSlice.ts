import {createSlice, PayloadAction} from "@reduxjs/toolkit";
import {appReducers, IAppState} from "../reducers/AppReducers";

const AppSlice = createSlice({
    name: 'App',
    initialState: {
        idle: false,
        loading: true,
        activeApp: ''
    } as IAppState,
    reducers: appReducers
});

export default AppSlice;
