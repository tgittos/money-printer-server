import {createSlice, PayloadAction} from "@reduxjs/toolkit";

export interface IAppState {
    loading: boolean;
    initialized: boolean;
}

const AppSlice = createSlice({
    name: 'App',
    initialState: {
        loading: true,
        initialized: false
    } as IAppState,
    reducers: {
        setAppInitialized(state: IAppState) {
            return {
                ...state,
                initialized: true,
                loading: false
            }
        },
        setAppLoading(state: IAppState, action: PayloadAction<boolean>) {
            return {
                ...state,
                loading: action.payload
            }
        }
    }
});

export const {
    setAppInitialized,
    setAppLoading
} = AppSlice.actions;
export default AppSlice.reducer;
