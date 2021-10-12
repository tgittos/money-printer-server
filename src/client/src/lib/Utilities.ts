import {
    Book, Calendar2Month, CashCoin, CashStack, CreditCard2Front, House, PiggyBank
} from "react-bootstrap-icons";

export function formatAsCurrency(num: number): string {
    return '$' + num.toFixed(2).replace(/(\d)(?=(\d{3})+(?!\d))/g, '$1,')
}

export function iconForAccountSubtype(subtype: string) {
    if (subtype === 'credit card') {
        return CreditCard2Front;
    }
    if (subtype === 'cd') {
        return Calendar2Month;
    }
    if (subtype === "money market") {
        return CashCoin;
    }
    if (subtype === "mortgage") {
        return House;
    }
    if (["401k", "ira"].includes(subtype)) {
        return PiggyBank;
    }
    if (subtype === "student") {
        return Book;
    }
    return CashStack;
}

export function modelToInterface<T, I>(data: T | T[], mapper: (m: T) => I): I | I[] {
    if (!(data as any).push) {
        data = [data as T];
    }

    const interfaces = (data as T[]).map(mapper);

    if (interfaces.length == 1) {
        return interfaces[0];
    }

    return interfaces;
}

// todo: figure out how to type the thunkApi
export const wrapThunk = function <T>(key: string, fn: (args: any, thunkApi: any) => Promise<T>) {
    return async (pArgs: any, pThunkApi: any) => {
        try {
            const state = pThunkApi.getState()[key];
            state.loading = true;
            return await fn(pArgs, pThunkApi);
        } catch (e) {
            return pThunkApi.rejectWithValue(e);
        }
    }
}

export function withType<T>() {
    return (a: T) => ({
        payload: a
    });
}
