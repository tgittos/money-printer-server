import {IBalance} from "../models/Balance";

interface IGetAccountBalancesResponse {
    success: boolean;
    message: string;
    data: IBalance[]
}

export default IGetAccountBalancesResponse;
