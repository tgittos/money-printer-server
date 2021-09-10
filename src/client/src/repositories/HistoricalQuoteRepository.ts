import BaseRepository from "./BaseRepository";
import ISymbolResponse from "../responses/SymbolsResponse";
import HistoricalIntradaySymbol, {IServerHistoricalIntradaySymbol} from "../models/symbols/HistoricalIntradaySymbol";
import IHistoricalIntradayResponse, {IRawHistoricalIntradayResponse} from "../responses/HistoricalIntradayResponse";

class LiveQuoteRepository extends BaseRepository {

    constructor() {
        super();

        this.apiEndpoint = "symbols";
    }

    public async historicalIntraday(symbol: string, start: Date): Promise<IHistoricalIntradayResponse> {
        const startTs = start.getTime() / 1000;
        const response = this.authenticatedRequest<null, IRawHistoricalIntradayResponse>({
            method: "GET",
            url: this.getSymbolEndpoint(symbol) + "/intraday?start=" + startTs,
        }).then(response => (response.data as unknown) as IRawHistoricalIntradayResponse)
          .then(response => {
            return {
                success: response.success,
                data: JSON.parse(response.data)
                    .map((obj: IServerHistoricalIntradaySymbol) => new HistoricalIntradaySymbol(symbol, obj))
                    .reverse()
            } as IHistoricalIntradayResponse
        });
        return response;
    }

    private getSymbolEndpoint(symbol: string) {
        return this.endpoint + "/" + symbol;
    }
}

export default LiveQuoteRepository;
