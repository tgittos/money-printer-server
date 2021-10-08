import {AnyAction, configureStore, ThunkDispatch} from '@reduxjs/toolkit';
import appReducer from './AppReducer';

const appStore = configureStore({
    reducer: appReducer,
});

// Infer the `RootState` and `AppDispatch` types from the store itself
export type AppState = ReturnType<typeof appStore.getState>
export type AppDispatch = typeof appStore.dispatch & ThunkDispatch<AppState, null, AnyAction>

export default appStore;
