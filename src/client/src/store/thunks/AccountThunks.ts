import {createAsyncThunk, PayloadAction} from "@reduxjs/toolkit";
import {IAccount} from "../../models/Account";
import {IAccountState} from "../reducers/AccountReducers";
import HttpService from "../../services/HttpService";
import IAuthProfileResponse from "../../responses/AuthProfileResponse";
import IListAccountsResponse from "../../responses/ListAccountsResponse";

const http = new HttpService();

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

// todo: figure out how to type the thunkApi
const wrapThunk = function <T>(fn: (args: any, thunkApi: any) => Promise<T>) {
    return async (pArgs: any, pThunkApi: any) => {
        try {
            const state: IAccountState = pThunkApi.getState().accounts;
            state.loading = true;
            return await fn(pArgs, pThunkApi);
        } catch (e) {
            return pThunkApi.rejectWithValue(e);
        }
    }
}

export const GetAccounts = createAsyncThunk<IAccount[]>(
    'accounts/listAccounts', wrapThunk<IAccount[]>(async (_: void, thunkApi) => {
        const response = await http.authenticatedRequest<void, IListAccountsResponse>({
                method: "GET",
                url: this.http.baseApiEndpoint + "/accounts"
            }).then(response => (response.data as unknown) as IListAccountsResponse);
        if (!response.success) {
            return thunkApi.rejectWithValue(response.message);
        }
        return response.data;
    }), globalThunkOptions);

export const RefreshAccountDetails = createAsyncThunk<IAccount>(
    'accounts/refreshAccountDetails', wrapThunk<IAccount>(async (accountId: number, thunkApi) => {
        const response = await http.authenticatedRequest<void, IListAccountsResponse>({
                method: "GET",
                url: this.http.baseApiEndpoint + "/accounts/" + accountId
            }).then(response => (response.data as unknown) as IAuthProfileResponse);
        if (!response.success) {
            return thunkApi.rejectWithValue(response.message);
        }
        return response.data;
    }), globalThunkOptions);
