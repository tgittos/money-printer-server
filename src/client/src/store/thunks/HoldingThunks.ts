import Holding, {IHolding} from "../../models/Holding";
import Env from "../../env";
import GetAccountHoldingsResponse from "../../responses/GetAccountHoldingsResponse";
import {createAsyncThunk} from "@reduxjs/toolkit";
import {wrapThunk} from "../../lib/Utilities";
import HttpService from "../../services/HttpService";

const http = new HttpService();

export const GetHoldingsForAccount = createAsyncThunk<IHolding[]>(
    'holdings/getForAccount', wrapThunk<IHolding[]>('holdings', async (accountId: number, thunkApi) => {
        if (Env.DEBUG) {
            console.log('AccountRepository::getHoldings - getting holdings for account id:', accountId);
        }
        const response = await http.authenticatedRequest<null, GetAccountHoldingsResponse>({
            url: http.baseApiEndpoint + "/accounts/" + accountId + "/holdings",
            method: "GET"
        }).then(response => (response as any).data as GetAccountHoldingsResponse);

        if (response.success) {
            // dispatch(AddHoldings(response.data));
        } else {
            return thunkApi.rejectWithValue(response.message)
        }
    }));





