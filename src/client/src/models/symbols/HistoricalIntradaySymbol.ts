import moment from 'moment';
import ISymbol from "../../interfaces/ISymbol";

export interface IHistoricalIntradaySymbol {
    symbol: string;
    date: string | Date;
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

class HistoricalIntradaySymbol implements ISymbol {
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
    public label: string;

    readonly _date: string;
    private _label: string;

    public get date(): Date {
        if (this._date && this._date != '') {
            return moment.utc(this._date).toDate();
        }

        const sansMeridianParts = this._label.split(' ');
        let sansMeridian = sansMeridianParts[0];
        if (sansMeridian.length == 1) {
            if (sansMeridianParts[1] == "PM") {
                sansMeridian = (parseInt(sansMeridian, 10) + 12).toString();
            }
            sansMeridian += ":00";
        }
        const dateToParse = `${this._date} ${sansMeridian}`;
        const date = moment(dateToParse).toDate();
        if (date === undefined) {
            console.log('couldn\'t parse date', dateToParse);
        }
        return date;
    }

    constructor(ticker: string, obj: IHistoricalIntradaySymbol) {
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

        this._date = obj.date as string;
        this._label = obj.label;
    }
}

export default HistoricalIntradaySymbol;
