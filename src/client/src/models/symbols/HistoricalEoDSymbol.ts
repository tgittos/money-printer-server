import moment from 'moment';
import ISymbol from "../../interfaces/ISymbol";

export interface IHistoricalEoDSymbol {
    symbol: string;
    date: string;
    label: string;
    average: number;
    changeOverTime: number;
    open: number;
    close: number;
    high: number;
    low: number;
    marketAverage: number;
    marketChangeOverTime: number;
    marketOpen: number
    marketClose: number;
    marketHigh: number;
    marketLow: number;
    marketNotional: number;
    marketNumberOfTrades: number;
    notional: number;
    numberOfTrades: number;
    volume: number;
}

class HistoricalEoDSymbol implements ISymbol {
    public symbol: string;
    public average: number;
    public changeOverTime: number;
    public open: number;
    public close: number;
    public high: number;
    public low: number;
    public marketAverage: number;
    public marketChangeOverTime: number;
    public marketOpen: number
    public marketClose: number;
    public marketHigh: number;
    public marketLow: number;
    public marketNotional: number;
    public marketNumberOfTrades: number;
    public notional: number;
    public numberOfTrades: number;
    public volume: number;

    private _date: string;
    private _label: string;

    public get date(): Date {
        return moment(this._date).toDate();
    }

    constructor(ticker: string, obj: IHistoricalEoDSymbol) {
        this.symbol = ticker;
        this.average = obj.average;
        this.changeOverTime = obj.changeOverTime;
        this.open = obj.open;
        this.close = obj.close;
        this.high = obj.high;
        this.low = obj.low;
        this.marketAverage = obj.marketAverage;
        this.marketChangeOverTime = obj.marketChangeOverTime;
        this.marketOpen = obj.marketOpen;
        this.marketClose = obj.marketClose;
        this.marketHigh = obj.marketHigh;
        this.marketLow = obj.marketLow;
        this.marketNotional = obj.marketNotional;
        this.marketNumberOfTrades = obj.marketNumberOfTrades;
        this.notional = obj.notional;
        this.numberOfTrades = obj.numberOfTrades;
        this.volume = obj.volume;

        this._date = obj.date;
        this._label = obj.label;
    }
}

export default HistoricalEoDSymbol;
