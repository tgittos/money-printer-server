import Balance from "../models/Balance";
import GetAccountBalancesResponse from "../responses/GetAccountBalancesResponse";
import HttpService from "./HttpService";

class AccountService {

    private http: HttpService;

    constructor() {
    }

    public async refreshAccountDetails(accountId: number): Promise<void> {
    }

    public async getBalanceHistoryForAccount(accountId: number, start: Date | null = null, end: Date | null = null): Promise<void> {

    }
}

export default AccountService;