import BaseRepository from "./BaseRepository";
import ListAccountsResponse from "../responses/ListAccountsResponse";
import Account from "../models/Account";
import AppStore from "../stores/AppStore"
import {setAccounts} from "../slices/AccountSlice";

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
}

export default AccountRepository;