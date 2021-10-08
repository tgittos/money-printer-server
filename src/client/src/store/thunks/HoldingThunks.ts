import Holding, {IHolding} from "../../models/Holding";
import Env from "../../env";
import GetAccountHoldingsResponse from "../../responses/GetAccountHoldingsResponse";
import {createAsyncThunk} from "@reduxjs/toolkit";
import {wrapThunk} from "../../utilities";
import HttpService from "../../services/HttpService";
import {useAppDispatch} from "../AppHooks";

const http = new HttpService();
const dispatch = useAppDispatch();

const globalThunkOptions = {
    condition(args , thunkApi): boolean | undefined {
        /*
        const { accounts } = thunkApi.getState();
        const inFlight = accounts.requests.length > 0;
        if (inFlight) {
            return false;
        }
         */
        return true;
    }
}

export const GetHoldingsForAccount = createAsyncThunk<IHolding[]>(
    'holdings/getForAccount', wrapThunk<IHolding[]>('holdings', async (accountId: number, thunkApi) => {
        if (Env.DEBUG) {
            console.log('AccountRepository::getHoldings - getting holdings for account id:', accountId);
        }
        const response = await this.authenticatedRequest<null, GetAccountHoldingsResponse>({
            url: http.baseApiEndpoint + "/accounts/" + accountId + "/holdings",
            method: "GET"
        }).then(response => (response as any).data as GetAccountHoldingsResponse);

        if (response.success) {
            dispatch(AddHoldings(response.data));
        } else {
            return thunkApi.rejectWithValue(response.message)
        }
    }, globalThunkOptions));





