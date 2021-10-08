import {createAsyncThunk, PayloadAction} from "@reduxjs/toolkit";
import Profile, {IAuthedProfile, IProfile} from "../../models/Profile";
import {useAppDispatch} from "../AppHooks";
import IAuthProfileRequest from "../../requests/AuthProfileRequest";
import IAuthProfileResponse from "../../responses/AuthProfileResponse";
import HttpService from "../../services/HttpService";
import IGetUnauthenticatedProfileResponse from "../../responses/GetUnauthenticatedProfileResponse";
import {wrapThunk} from "../../utilities";

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

export const InitializeUnauthenticated = createAsyncThunk<IProfile>(
    'profile/getUnauthenticatedProfile', wrapThunk<IProfile>('profile', async (_, thunkApi) => {
        const response = await this.unauthenticatedRequest<null, IGetUnauthenticatedProfileResponse>({
            url: this.http.baseApiEndpoint + "/profile/unauthenticated"
        }).then(response => (response.data as unknown) as IGetUnauthenticatedProfileResponse);
        if (response.success) {
            const unauthedProfile = new Profile(response.data.profile);
            return unauthedProfile;
        } else {
            return thunkApi.rejectWithValue(response.message);
        }
    }), globalThunkOptions);

export const AuthenticateUser = createAsyncThunk<IAuthedProfile, { username: string, password: string }>(
    'profile/authenticate', wrapThunk<IAuthedProfile>('profile', async ({ username, password }, thunkApi) => {
        const response = await http.unauthenticatedRequest<IAuthProfileRequest, IAuthProfileResponse>({
                method: "POST",
                url: this.endpoint + "/login",
                data: { username, password }
            })
            .then(response => (response.data as unknown) as IAuthProfileResponse);
        if (!response.success) {
            return thunkApi.rejectWithValue(response.message);
        }
        return response.data;
    }), globalThunkOptions);
