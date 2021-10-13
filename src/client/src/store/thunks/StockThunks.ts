import {IHistoricalEoDSymbol} from "../../models/symbols/HistoricalEoDSymbol";
import IHistoricalEoDResponse from "../../responses/HistoricalEoDResponse";
import moment from "moment";
import {IHistoricalIntradaySymbol} from "../../models/symbols/HistoricalIntradaySymbol";
import IHistoricalIntradayResponse from "../../responses/HistoricalIntradayResponse";
import HttpService from "../../services/HttpService";
import {createAsyncThunk} from "@reduxjs/toolkit";
import {wrapThunk} from "../../lib/Utilities";

const http = new HttpService();

export const GetSymbolPreviousClose = createAsyncThunk<IHistoricalEoDSymbol>(
    'stock/getSymbolPreviousClose', wrapThunk<IHistoricalEoDSymbol>('stocks', async (symbol: string, thunkApi) => {
        if (symbol === null || symbol === undefined || symbol === '') {
            throw Error(`cannot fetch previous for invalid symbol: ${symbol}`);
        }

        const response = await http.authenticatedRequest<null, IHistoricalEoDResponse>({
            method: "GET",
            url: http.baseApiEndpoint + "/symbols/" + symbol + "/previous"
        }).then(response => (response.data as unknown) as IHistoricalEoDResponse);

        if (response.success) {
            return response.data[0];
        } else {
            console.log('StockService::previous - error fetching previous for symbol', symbol, response.message);
            return thunkApi.rejectWithValue(response.message);
        }
}));

export const GetSymbolHistoricalCloses = createAsyncThunk<IHistoricalEoDSymbol[]>(
    'stock/getSymbolHistoricalClose', wrapThunk<IHistoricalEoDSymbol[]>('stocks', async (args, thunkApi) => {
        const { symbol, start, end } = args;

        const startTs = moment(start).utc().toDate().getTime() / 1000.0;
        const endTs = moment(end ?? moment.utc()).utc().toDate().getTime() / 1000.0;

        const response = await http.authenticatedRequest<null, IHistoricalEoDResponse>({
            method: "GET",
            url: http.baseApiEndpoint + "/symbols/" + symbol + "/eod?start=" + startTs + "&end=" + endTs
        }).then(response => (response.data as unknown) as IHistoricalEoDResponse);

        if (!response.success) {
        console.log('StockService::historicalEoD - error fetching historicalEoD for symbol',
            symbol,
            'over period',
            startTs,
            endTs,
            response.message);
        return [] as IHistoricalEoDSymbol[];
    }

    return response.data;
}));

export const GetSymbolHistoricalIntraday = createAsyncThunk<IHistoricalIntradaySymbol[]>(
    'stock/getSymbolHistoricalIntraday', wrapThunk<IHistoricalIntradaySymbol[]>('stocks', async (args, thunkApi) => {
        const { symbol, start } = args;

        const startTs = start.getTime() / 1000;

        const response = await http.authenticatedRequest<null, IHistoricalIntradayResponse>({
            method: "GET",
            url: http.baseApiEndpoint + "/symbols/" + symbol +"/intraday?start=" + startTs,
        }).then(response => (response.data as unknown) as IHistoricalIntradayResponse)

        if (response.success) {
            return response.data;
        } else {
            console.log('StockService::historicalIntraday - error fetching historicalIntraday for symbol',
                symbol,
                'since',
                startTs,
                response.message);
            return thunkApi.rejectWithValue(response.message);
        }
}));
