import BaseRepository from "./BaseRepository";
import ListAccountsResponse from "../responses/ListAccountsResponse";
import Account from "../models/Account";
import AppStore, {getProfileState} from "../stores/AppStore"
import {
    IAccountBalance,
    IAccountHolding,
    setAccounts,
    setBalances,
    setHoldings
} from "../slices/AccountSlice";
import Balance from "../models/Balance";
import GetAccountBalancesResponse from "../responses/GetAccountBalancesResponse";
import Holding from "../models/Holding";
import GetAccountHoldingsResponse from "../responses/GetAccountHoldingsResponse";
import Env from "../env";

class AccountRepository extends BaseRepository {
    constructor() {
        super();

        this.apiEndpoint = "accounts";
    }

    public async listAccounts(): Promise<Account[]> {
        const response = await this.authenticatedRequest<null, ListAccountsResponse>({
            url: this.endpoint,
            method: "GET"
        }).then(response => (response as any).data as ListAccountsResponse);

        if (response.success) {
            const accounts = response.data.map(serverObj => new Account(serverObj));
            AppStore.dispatch(setAccounts(response.data));
            accounts.forEach(account => {
                this.getBalances(account.id);
                if (account.type === "investment") {
                    this.getHoldings(account.id);
                }
            });
            return accounts;
        }

        AppStore.dispatch(setAccounts([]))
        return [];
    }

    public async refreshAccounts(accountId: number): Promise<void> {
        console.log('refreshing account', accountId)
    }

    public async getBalances(accountId: number, start: Date | null = null, end: Date | null = null): Promise<Balance[]> {
        if (start === null && end !== null) {
            throw new Error("can't request balances with a given end without a given start");
        }

        let url = this.endpoint + "/" + accountId + "/balances";

        if (start !== null) {
            url += "?start=" + start.getTime() / 1000.0;
        }
        if (end !== null) {
            url += "&end=" + end.getTime() / 1000.0;
        }

        const response = await this.authenticatedRequest<null, GetAccountBalancesResponse>({
            url: url,
            method: "GET"
        }).then(response => (response as any).data as GetAccountBalancesResponse);

        const balances = response.data.map(obj => new Balance(obj));

        AppStore.dispatch(setBalances({ accountId, balances: response.data } as IAccountBalance));

        return balances;
    }

    public async getHoldings(accountId: number): Promise<Holding[]> {
        if (Env.DEBUG) {
            console.log('AccountRepository::getHoldings - getting holdings for account id:', accountId);
        }
        const response = await this.authenticatedRequest<null, GetAccountHoldingsResponse>({
            url: this.endpoint + "/" + accountId + "/holdings",
            method: "GET"
        }).then(response => (response as any).data as GetAccountHoldingsResponse);

        const holdings = response.data.map(obj => new Holding(obj));

        AppStore.dispatch(setHoldings({ accountId, holdings: response.data } as IAccountHolding));

        return holdings;
    }
}

export default AccountRepository;