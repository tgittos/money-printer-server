import {IBalance} from "../models/Balance";

interface IGetAccountBalancesResponse {
    success: boolean;
    data: IBalance[]
}

export default IGetAccountBalancesResponse;
