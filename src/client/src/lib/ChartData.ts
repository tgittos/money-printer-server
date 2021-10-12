import ISymbol from "../interfaces/ISymbol";
import ILineDataPoint from "../components/shared/Charts/interfaces/ILineDataPoint";
import ICandleDataPoint from "../components/shared/Charts/interfaces/ICandleDataPoint";
import {IHistoricalEoDSymbol} from "../models/symbols/HistoricalEoDSymbol";
import {IHistoricalIntradaySymbol} from "../models/symbols/HistoricalIntradaySymbol";
import {IBalance} from "../models/Balance";

export type SymbolType = IHistoricalEoDSymbol | IHistoricalIntradaySymbol;

export function formatSymbolsForLine(data: SymbolType[]): ILineDataPoint[] {
    const formattedData = data.map(datum => {
        return {
            x: datum.date,
            y: datum.close
        } as ILineDataPoint;
    });
    return formattedData;
}

export function formatSymbolsForCandle(data: SymbolType[]): ICandleDataPoint[] {
    const formattedData = data.map(datum => {
        const datapoint = {
            x: datum.date,
            open: datum.open,
            close: datum.close,
            high: datum.high,
            low: datum.low,
        } as unknown as ICandleDataPoint;

        // this seems fishy too on some tickers, like MIPTX
        if (datapoint.low == 0) {
            datapoint.low = Math.min(datapoint.open, datapoint.close);
        }

        return datapoint;
    });
    return formattedData;
}

export function formatBalancesForLine(data: IBalance[]): ILineDataPoint[] {
    const formattedData = data.map(datum => {
        return {
            x: datum.timestamp,
            y: datum.current
        } as ILineDataPoint;
    });
    return formattedData;
}
