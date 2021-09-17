import {IServerHistoricalEoDSymbol} from "../models/symbols/HistoricalEoDSymbol";

interface IHistoricalEoDResponse {
    success: boolean;
    message: string;
    data: IServerHistoricalEoDSymbol[];
}

export default IHistoricalEoDResponse;
