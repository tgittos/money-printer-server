import {IAccount} from "../models/Account";

interface IListAccountsResponse {
    success: boolean;
    data: IAccount[];
}

export default IListAccountsResponse;
