import IAccount from "../interfaces/IAccount";

interface IPlaidSetAccessTokenResponse {
    success: boolean;
    data: IAccount;
}

export default IPlaidSetAccessTokenResponse;