import {IAccount} from "../models/Account";

interface IListAccountsResponse {
    success: boolean;
    message: string;
    data: IAccount[];
}

export default IListAccountsResponse;
