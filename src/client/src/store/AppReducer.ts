import { combineReducers } from "redux";
import AppSlice from "slices/AppSlice";
import ProfileSlice from "slices/ProfileSlice";
import PlaidSlice from "slices/PlaidSlice";
import AccountSlice from "slices/AccountSlice";
import BalanceSlice from "./slices/BalanceSlice";
import HoldingSlice from "./slices/HoldingSlice";
import StockSlice from "./slices/StockSlice";

const appReducer = combineReducers({
    app: AppSlice.reducer,
    profile: ProfileSlice.reducer,
    plaid: PlaidSlice.reducer,
    accounts: AccountSlice.reducer,
    balances: BalanceSlice.reducer,
    holdings: HoldingSlice.reducer,
    stocks: StockSlice.reducer
});

export type AppState = ReturnType<typeof appReducer>;
export default appReducer;
