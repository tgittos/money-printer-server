import Profile, {IProfile} from "../models/Profile";
import {createSlice, PayloadAction} from "@reduxjs/toolkit";
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
    initialState: {
        authenticated: false,
        current: null
    } as IProfileState,
    reducers: {
        setCurrentProfile: {
            reducer: (state : IProfileState, action: PayloadAction<IProfile>) => {
                if (Env.DEBUG) {
                    console.log('ProfileSlice::setCurrentProfile - got action:', action)
                }
                return {
                    ...state,
                    current: action.payload,
                    authenticated: action.payload?.id !== null,
                    loading: false
                };
            },
            prepare: (profile: IProfile) => {
                return {
                    payload: {
                        id: profile.id,
                        firstName: profile.firstName,
                        lastName: profile.lastName,
                        username: profile.username,
                        timestamp: profile.timestamp
                    } as IProfile
                };
            }
        },
        clearCurrentProfile: (state: IProfileState) => {
            if (Env.DEBUG) {
                console.log('ProfileSlice::clearCurrentProfile');
            }
            return {
                ...state,
                current: null,
                authenticated: false,
                loading: false
            }
        }
    }
});

export const { setCurrentProfile, clearCurrentProfile } = ProfileSlice.actions;
export default ProfileSlice.reducer;