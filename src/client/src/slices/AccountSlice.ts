import {createSlice, PayloadAction} from "@reduxjs/toolkit";
import IAccount from "../interfaces/IAccount";
import Account from "../models/Account";
import Balance, {IBalance} from "../models/Balance";
import Holding, {IHolding} from "../models/Holding";

export interface IAccountBalance {
    accountId: number;
    balances: IBalance[];
}

export interface IAccountHolding {
    accountId: number;
    holdings: IHolding[];
}

export interface IAccountState {
    accounts: IAccount[];
    balances: IAccountBalance[];
    holdings: IAccountHolding[];
}

// convert a given Account or Account[] to the appropriate
// IAccount or IAccount[] response
function modelToInterface<T, I>(data: T | T[], mapper: (m: T) => I): I | I[] {
    if (!(data as any).push) {
        data = [data as T];
    }

    const interfaces = (data as T[]).map(mapper);

    if (interfaces.length == 1) {
        return interfaces[0];
    }

    return interfaces;
}

export function accountToIAccount(data: Account | Account[]): IAccount | IAccount[] {
   return modelToInterface<Account, IAccount>(data, (account => ({
       id: account.id,
       name: account.name,
       type: account.type,
       subtype: account.subtype,
       balance: account.balance,
       timestamp: account.timestamp
   }) as IAccount));
}

export function balanceToIBalance(data: Balance | Balance[]): IBalance | IBalance[] {
    return modelToInterface<Balance, IBalance>(data, (balance => ({
        id: balance.id,
        accountId: balance.accountId,
        current: balance.current,
        timestamp: balance.timestamp
    }) as IBalance))
}

export function holdingToIHolding(data: Holding | Holding[]): IHolding | IHolding[] {
    return modelToInterface<Holding, IHolding>(data, (holding => ({
        id: holding.id,
        accountId: holding.accountId,
        securityId: holding.securityId,
        costBasis: holding.costBasis,
        quantity: holding.quantity,
        isoCurrencyCode: holding.isoCurrencyCode,
        timestamp: holding.timestamp
    }) as IHolding))
}

const AccountSlice = createSlice({
    name: 'Account',
    initialState: {
        accounts: [],
        balances: [],
        holdings: []
    } as IAccountState,
    reducers: {
        setAccounts(state: IAccountState, action: PayloadAction<IAccount[]>) {
            return {
                ...state,
                accounts: [].concat(action.payload)
            }
        },
        addAccount(state: IAccountState, action: PayloadAction<IAccount>) {
            return {
                ...state,
                accounts: [].concat(state.accounts).concat([action.payload])
            }
        },
        setBalances(state: IAccountState, action: PayloadAction<IAccountBalance>) {
            const accountId = action.payload.accountId;
            return {
                ...state,
                balances: state.balances
                    .filter(accountBalance => accountBalance.accountId !== accountId)
                    .concat({
                        accountId,
                        balances: action.payload.balances
                    } as IAccountBalance)
            }
        },
        setHoldings(state: IAccountState, action: PayloadAction<IAccountHolding>) {
            const accountId = action.payload.accountId;
            return {
                ...state,
                holdings: state.holdings
                    .filter(accountHoldings => accountHoldings.accountId !== accountId)
                    .concat({
                        accountId,
                        holdings: action.payload.holdings
                    } as IAccountHolding)
            }
        }
    }
});

export const {
    setAccounts,
    addAccount,
    setBalances,
    setHoldings
} = AccountSlice.actions;
export default AccountSlice.reducer;
