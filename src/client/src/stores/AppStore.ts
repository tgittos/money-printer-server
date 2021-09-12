import { configureStore } from '@reduxjs/toolkit';

import ProfileSlice from "./../slices/ProfileSlice";
import AppSlice from "./../slices/AppSlice";
import PlaidSlice from "../slices/PlaidSlice";

const appStore = configureStore({
    reducer: {
        app: AppSlice,
        profile: ProfileSlice,
        plaid: PlaidSlice
    }
});

export default appStore;
