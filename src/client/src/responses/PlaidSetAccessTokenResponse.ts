import {IAccount} from "../models/Account";

interface IPlaidSetAccessTokenResponse {
    success: boolean;
    data: IAccount;
}

export default IPlaidSetAccessTokenResponse;