import {createSlice, PayloadAction} from "@reduxjs/toolkit";
import {createHoldingThunks, holdingReducers, IHoldingState} from "../reducers/HoldingReducers";

const holdingSlice = createSlice({
    name: 'holdings',
    initialState: {
        idle: true,
        loading: false,
        holdings: []
    } as IHoldingState,
    reducers: holdingReducers,
    extraReducers: createHoldingThunks
});

export default holdingSlice;
