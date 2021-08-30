import Profile from "../models/Profile";
import {createSlice} from "@reduxjs/toolkit";

export interface IProfileState {
    loading: boolean;
    authenticated: boolean;
    current: Profile | null;
}

export interface IProfileAction {
    type: string,
    payload: Profile | null
}

const ProfileSlice = createSlice({
    name: 'Profile',
    initialState: {} as IProfileState,
    reducers: {
        setCurrentProfile: {
            reducer(state: IProfileState, action: IProfileAction) {
                return {
                    ...state,
                    current: action.payload,
                    authenticated: !!action.payload?.id,
                    loading: false
                }
            },
            prepare(profile: Profile) {
                return {
                    payload: profile
                };
            }
        }
    }
});

export const { setCurrentProfile } = ProfileSlice.actions;
export default ProfileSlice.reducer;