import GetAccountBalancesResponse from "../../responses/GetAccountBalancesResponse";
import Balance, {IBalance} from "../../models/Balance";
import HttpService from "../../services/HttpService";
import {createAsyncThunk} from "@reduxjs/toolkit";
import {wrapThunk} from "../../lib/Utilities";

const http = new HttpService();

export const GetBalanceHistoryForAccount = createAsyncThunk<IBalance[], { start: Date, end: Date, id: number}>(
    'balance/getHistoryForAccount', wrapThunk<IBalance[]>('balances', async (args, thunkApi) => {
        const { start, end, id } = args;
        if (start === null && end !== null) {
            throw new Error("can't request balances with a given end without a given start");
        }

        let url = http.baseApiEndpoint + "/accounts/" + id + "/balances";

        if (start !== null) {
            url += "?start=" + start.getTime() / 1000.0;
        }
        if (end !== null) {
            url += "&end=" + end.getTime() / 1000.0;
        }

        const response = await http.authenticatedRequest<null, GetAccountBalancesResponse>({
            url: url,
            method: "GET"
        }).then(response => (response as any).data as GetAccountBalancesResponse);

        if (response.success) {
            const balances = response.data.map(obj => new Balance(obj));
            return balances;
        } else {
            thunkApi.rejectWithValue(response.message);
        }

    }));

