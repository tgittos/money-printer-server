import IAccount from "../interfaces/IAccount";

interface IListAccountsResponse {
    success: boolean;
    data: IAccount[];
}

export default IListAccountsResponse;
