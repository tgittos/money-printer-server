import Profile from "../models/Profile";
import {createSlice} from "@reduxjs/toolkit";
import Env from "../env";

export interface IProfileState {
    loading: boolean;
    authenticated: boolean;
    exp: Date;
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
                if (Env.DEBUG) {
                    console.log('ProfileSlice::setCurrentProfile::reducer - got action:', action)
                }
                return {
                    ...state,
                    current: action.payload,
                    authenticated: action.payload?.id !== undefined,
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