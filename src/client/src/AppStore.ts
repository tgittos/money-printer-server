import { configureStore } from '@reduxjs/toolkit';

import ProfileSlice from "./slices/ProfileSlice";
import AppSlice from "./slices/AppSlice";

const appStore = configureStore({
    reducer: {
        app: AppSlice,
        profile: ProfileSlice
    }
});

export default appStore;
