import {IHistoricalIntradaySymbol} from "../models/symbols/HistoricalIntradaySymbol";

interface IHistoricalIntradayResponse {
    success: boolean;
    message: string;
    data: IHistoricalIntradaySymbol[];
}

export default IHistoricalIntradayResponse;
