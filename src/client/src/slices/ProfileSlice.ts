import Profile, {IProfile} from "../models/Profile";
import {createSlice, PayloadAction} from "@reduxjs/toolkit";
import Env from "../env";

export interface IProfileState {
    loading: boolean;
    authenticated: boolean;
    exp: Date;
    current: IProfile | null;
    unauthenticated: IProfile | null;
}

function profileToIProfile(profile: Profile): IProfile {
    if (profile == null) {
        return null;
    }

    return {
        id: profile.id,
        firstName: profile.firstName,
        lastName: profile.lastName,
        username: profile.username,
    } as IProfile;
}

const ProfileSlice = createSlice({
    name: 'Profile',
    initialState: {
        authenticated: false,
        current: null,
        unauthenticated: null
    } as IProfileState,
    reducers: {
        setUnauthenticatedProfile: {
          reducer: (state: IProfileState, action: PayloadAction<IProfile>) => {
              return {
                  ...state,
                  unauthenticated: action.payload
              };
          },
          prepare: (profile: Profile) => {
              return {
                  payload: profileToIProfile(profile)
              };
          }
        },
        setCurrentProfile: {
            reducer: (state : IProfileState, action: PayloadAction<IProfile>) => {
                return {
                    ...state,
                    current: action.payload,
                    authenticated: action.payload?.id !== null,
                    loading: false
                };
            },
            prepare: (profile: Profile) => {
                return {
                    payload: profileToIProfile(profile)
                };
            }
        },
        clearCurrentProfile: (state: IProfileState) => {
            return {
                ...state,
                current: state.unauthenticated,
                authenticated: false,
                loading: false
            }
        }
    }
});

export const {
    setUnauthenticatedProfile,
    setCurrentProfile,
    clearCurrentProfile
} = ProfileSlice.actions;
export default ProfileSlice.reducer;