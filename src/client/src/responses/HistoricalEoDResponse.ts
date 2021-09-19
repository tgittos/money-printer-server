import {IHistoricalEoDSymbol} from "../models/symbols/HistoricalEoDSymbol";

interface IHistoricalEoDResponse {
    success: boolean;
    message: string;
    data: IHistoricalEoDSymbol[];
}

export default IHistoricalEoDResponse;
