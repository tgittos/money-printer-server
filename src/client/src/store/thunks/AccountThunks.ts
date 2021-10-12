import {createAsyncThunk, PayloadAction} from "@reduxjs/toolkit";
import {IAccount} from "../../models/Account";
import {IAccountState} from "../reducers/AccountReducers";
import HttpService from "../../services/HttpService";
import IAuthProfileResponse from "../../responses/AuthProfileResponse";
import IListAccountsResponse from "../../responses/ListAccountsResponse";

const http = new HttpService();

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
                url: http.baseApiEndpoint + "/accounts"
            }).then(response => (response.data as unknown) as IListAccountsResponse);
        if (!response.success) {
            return thunkApi.rejectWithValue(response.message);
        }
        return response.data;
    }));

export const RefreshAccountDetails = createAsyncThunk<IAccount>(
    'accounts/refreshAccountDetails', wrapThunk<IAccount>(async (accountId: number, thunkApi) => {
        const response = await http.authenticatedRequest<void, IListAccountsResponse>({
                method: "GET",
                url: http.baseApiEndpoint + "/accounts/" + accountId
            }).then(response => (response.data as unknown) as IAuthProfileResponse);
        if (!response.success) {
            return thunkApi.rejectWithValue(response.message);
        }
        return response.data;
    }));
