import {createSlice} from "@reduxjs/toolkit";
import {IProfileState} from "./ProfileSlice";

export interface IAppState {
    profile: IProfileState
}

export interface IAppAction {
    type: string,
    payload: any
}

const AppSlice = createSlice({
    name: 'App',
    initialState: {
        profile: {
            loading: true
        }
    } as IAppState,
    reducers: {
        setLoading(state: IAppState, action: IAppAction) {
            return {
                ...state,
                loading: false
            }
        }
    }
});

export const { setLoading } = AppSlice.actions;
export default AppSlice.reducer;
