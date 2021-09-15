import {IServerHolding} from "../models/Holding";

interface IGetAccountHoldingsResponse {
    success: boolean;
    data: IServerHolding[];
}

export default IGetAccountHoldingsResponse
