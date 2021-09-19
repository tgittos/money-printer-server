import {IHolding} from "../models/Holding";

interface IGetAccountHoldingsResponse {
    success: boolean;
    data: IHolding[];
}

export default IGetAccountHoldingsResponse
