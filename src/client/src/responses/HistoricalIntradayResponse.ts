import {IServerHistoricalIntradaySymbol} from "../models/symbols/HistoricalIntradaySymbol";

export interface IRawHistoricalIntradayResponse {
    success: boolean;
    message: string;
    data: string;
}

interface IHistoricalIntradayResponse {
    success: boolean;
    message: string;
    data: IServerHistoricalIntradaySymbol[];
}

export default IHistoricalIntradayResponse;
