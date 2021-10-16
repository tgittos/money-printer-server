import { combineReducers } from "redux";
import BalanceSlice from "./slices/BalanceSlice";
import HoldingSlice from "./slices/HoldingSlice";
import StockSlice from "./slices/StockSlice";
import AppSlice from "./slices/AppSlice";
import ProfileSlice from "./slices/ProfileSlice";
import PlaidSlice from "./slices/PlaidSlice";
import AccountSlice from "./slices/AccountSlice";

const appReducer = combineReducers({
    app: AppSlice.reducer,
    profile: ProfileSlice.reducer,
    plaid: PlaidSlice.reducer,
    accounts: AccountSlice.reducer,
    balances: BalanceSlice.reducer,
    holdings: HoldingSlice.reducer,
    stocks: StockSlice.reducer
});

export default appReducer;
