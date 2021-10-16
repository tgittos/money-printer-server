import {IHolding} from "../models/Holding";

interface IGetAccountHoldingsResponse {
    success: boolean;
    message?: string;
    data: IHolding[];
}

export default IGetAccountHoldingsResponse
