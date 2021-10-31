import {IProfile} from "../../models/Profile";
import {createContext, Dispatch} from "react";

interface ProfileState {
    current: IProfile;
    authenticated: boolean;
}

export interface ProfileAction {
    type: string;
    payload: IProfile
}

export const SET_PROFILE: string = "set_profile";

export const initialProfileState: ProfileState = {
    current: null,
    authenticated: false
};

export const ProfileContext = createContext<{
    state: ProfileState,
    dispatch: Dispatch<ProfileAction>
}>({
    state: initialProfileState,
    dispatch: () => undefined,
});

export const profileReducer = (state: ProfileState, action: ProfileAction) => {
    switch(action.type) {
        case SET_PROFILE:
            return {
                ...state,
                current: action.payload
            } as ProfileState
        default:
            throw new Error("unhandled action type");
    }
}
