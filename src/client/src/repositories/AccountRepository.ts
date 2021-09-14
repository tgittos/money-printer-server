import BaseRepository from "./BaseRepository";
import ListAccountsResponse from "../responses/ListAccountsResponse";
import Account from "../models/Account";
import AppStore from "../stores/AppStore"
import {setAccounts} from "../slices/AccountSlice";
import Balance from "../models/Balance";
import GetAccountBalancesResponse from "../responses/GetAccountBalancesResponse";
import moment from "moment";

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
            AppStore.dispatch(setAccounts(accounts));
            return accounts;
        }

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

        return balances;
    }
}

export default AccountRepository;