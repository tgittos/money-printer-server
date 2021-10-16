import {createAsyncThunk, PayloadAction} from "@reduxjs/toolkit";
import Profile, {IAuthedProfile, IProfile} from "../../models/Profile";
import IAuthProfileRequest from "../../requests/AuthProfileRequest";
import IAuthProfileResponse from "../../responses/AuthProfileResponse";
import HttpService from "../../services/HttpService";
import IGetUnauthenticatedProfileResponse from "../../responses/GetUnauthenticatedProfileResponse";
import {wrapThunk} from "../../lib/Utilities";

const http = new HttpService();

export const InitializeUnauthenticated = createAsyncThunk<IProfile>(
    'profile/getUnauthenticatedProfile', wrapThunk<IProfile>('profile', async (_, thunkApi) => {

        const response = await http.unauthenticatedRequest<null, IGetUnauthenticatedProfileResponse>({
            url: http.baseApiEndpoint + "/profile/unauthenticated"
        }).then(response => (response.data as unknown) as IGetUnauthenticatedProfileResponse);
        if (response.success) {
            const unauthedProfile = new Profile(response.data.profile);
            return unauthedProfile;
        } else {
            return thunkApi.rejectWithValue(response.message);
        }

    }));

export const AuthenticateUser = createAsyncThunk<IAuthedProfile, { username: string, password: string }>(
    'profile/authenticate', wrapThunk<IAuthedProfile>('profile', async ({ username, password }, thunkApi) => {
        const response = await http.unauthenticatedRequest<IAuthProfileRequest, IAuthProfileResponse>({
                method: "POST",
                url: http.baseApiEndpoint + "/auth/login",
                data: { username, password }
            })
            .then(response => (response.data as unknown) as IAuthProfileResponse);
        if (!response.success) {
            return thunkApi.rejectWithValue(response.message);
        }
        return response.data;
    }));
