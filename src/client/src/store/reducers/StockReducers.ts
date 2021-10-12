import {GetAccounts, RefreshAccountDetails} from "../thunks/AccountThunks";
import {PayloadAction} from "@reduxjs/toolkit";
import {IAccount} from "../../models/Account";
import {AddAccounts} from "../actions/AccountActions";
import {GetSymbolHistoricalCloses, GetSymbolHistoricalIntraday, GetSymbolPreviousClose} from "../thunks/StockThunks";
import {IHistoricalIntradaySymbol} from "../../models/symbols/HistoricalIntradaySymbol";
import {IHistoricalEoDSymbol} from "../../models/symbols/HistoricalEoDSymbol";
import HttpService from "../../services/HttpService";

export interface IStockIntradays {
    symbol: string;
    prices: IHistoricalIntradaySymbol[];
}

export interface IStockEoDs {
    symbol: string;
    prices: IHistoricalEoDSymbol[];
}

export interface IStockState {
    idle: boolean;
    loading: boolean;
    error: string;

    intradays: IStockIntradays[];
    eods: IStockEoDs[];
}

export const stockReducers = {

};

export const createStockThunks = ((builder: any) =>
        builder
            .addCase(GetSymbolPreviousClose.fulfilled, (state: IStockState, action: PayloadAction<IHistoricalEoDSymbol>) => {

                state.loading = false;
            })
            .addCase(GetSymbolPreviousClose.rejected, (state: IStockState, action: string) => {
                state.error = action;
                state.loading = false;
            })
            .addCase(GetSymbolHistoricalCloses.fulfilled, (state: IStockState, action: PayloadAction<IHistoricalEoDSymbol[]>) => {
                state.error = '';
                state.loading = false;
            })
            .addCase(GetSymbolHistoricalCloses.rejected, (state: IStockState, action: string) => {
                state.error = action;
                state.loading = false;
            })
            .addCase(GetSymbolHistoricalIntraday.fulfilled, (state: IStockState, action: PayloadAction<IHistoricalIntradaySymbol[]>) => {

            })
            .addCase(GetSymbolHistoricalIntraday.rejected, (state: IStockState, action: string) => {
                state.error = action;
                state.loading = false;
            })
);

