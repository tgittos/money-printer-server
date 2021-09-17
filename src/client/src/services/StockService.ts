import HttpService from "./HttpService";
import IHistoricalEoDResponse from "../responses/HistoricalEoDResponse";
import moment from "moment";
import IHistoricalIntradayResponse, {IRawHistoricalIntradayResponse} from "../responses/HistoricalIntradayResponse";
import HistoricalIntradaySymbol, {IServerHistoricalIntradaySymbol} from "../models/symbols/HistoricalIntradaySymbol";
import {IServerHistoricalEoDSymbol} from "../models/symbols/HistoricalEoDSymbol";

class StockService {

    private http: HttpService;
    private stockEndpoint: string = "symbols"

    private getSymbolEndpoint(symbol: string) {
        return this.http.baseApiEndpoint + "/" + this.stockEndpoint + "/" + symbol;
    }

    constructor() {
        this.http = new HttpService();
    }

    public async previous(symbol: string): Promise<IServerHistoricalEoDSymbol> {
        if (symbol === null || symbol === undefined || symbol === '') {
            throw Error(`cannot fetch previous for invalid symbol: ${symbol}`);
        }

        const response = await this.http.authenticatedRequest<null, IHistoricalEoDResponse>({
            method: "GET",
            url: this.getSymbolEndpoint(symbol) + "/previous"
        }).then(response => (response.data as unknown) as IHistoricalEoDResponse);

        if (!response.success) {
            console.log('StockService::previous - error fetching previous for symbol', symbol, response.message);
            return null;
        }

        return response.data[0];
    }

    public async historicalEoD(symbol: string, start: Date | null = null, end: Date | null = null):
        Promise<IServerHistoricalEoDSymbol[]> {

        const startTs = moment(start).seconds()
        const endTs = moment(end ?? moment(start).subtract(7, 'days')).seconds()

        const response = await this.http.authenticatedRequest<null, IHistoricalEoDResponse>({
            method: "GET",
            url: this.getSymbolEndpoint(symbol) + "/eod?start=" + startTs + "&end=" + endTs
        }).then(response => (response.data as unknown) as IHistoricalEoDResponse);

        if (!response.success) {
            console.log('StockService::historicalEoD - error fetching historicalEoD for symbol',
                symbol,
                'over period',
                startTs,
                endTs,
                response.message);
            return [];
        }

        return response.data;
    }


    public async historicalIntraday(symbol: string, start: Date): Promise<IServerHistoricalIntradaySymbol[]> {

        const startTs = start.getTime() / 1000;

        const response = await this.http.authenticatedRequest<null, IHistoricalIntradayResponse>({
            method: "GET",
            url: this.getSymbolEndpoint(symbol) + "/intraday?start=" + startTs,
        }).then(response => (response.data as unknown) as IHistoricalIntradayResponse)

        if (!response.success) {
            console.log('StockService::historicalIntraday - error fetching historicalIntraday for symbol',
                symbol,
                'since',
                startTs,
                response.message);
            return [];
        }

        return response.data;
    }
}

export default StockService;