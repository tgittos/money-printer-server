import {createSlice, PayloadAction} from "@reduxjs/toolkit";
import {createStockThunks, IStockState, stockReducers} from "../reducers/StockReducers";

const stockSlice = createSlice({
    name: 'stocks',
    initialState: {
        idle: true,
        loading: false,
        eods: [],
        intradays: []
    } as IStockState,
    reducers: stockReducers,
    extraReducers: createStockThunks
});

export default stockSlice;
