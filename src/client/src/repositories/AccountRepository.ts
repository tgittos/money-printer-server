import BaseRepository from "./BaseRepository";
import ListAccountsResponse from "../responses/ListAccountsResponse";
import Account from "../models/Account";

class AccountRepository extends BaseRepository {
    constructor() {
        super();

        this.apiEndpoint = "accounts";
    }

    public async listAccounts(): Promise<Account[]> {
        const response = await this.authenticatedRequest<null, ListAccountsResponse>({
            url: this.endpoint,
            method: "GET"
        }).then(response => (response as unknown).data as ListAccountsResponse);

        if (response.success) {
            return response.data.map(serverObj => new Account(serverObj));
        }

        return [];
    }
}

export default AccountRepository;