import {createSlice, PayloadAction} from "@reduxjs/toolkit";

export interface IPlaidState {
    linkToken: string;
}

const PlaidSlice = createSlice({
    name: 'Plaid',
    initialState: {
        linkToken: ''
    } as IPlaidState,
    reducers: {
        setLinkToken(state: IPlaidState, action: PayloadAction<string>) {
            return {
                ...state,
                linkToken: action.payload
            }
        },
    }
});

export default PlaidSlice;
