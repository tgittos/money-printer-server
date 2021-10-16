import HttpService from "./HttpService";
import {BehaviorSubject, Observable, Subscription} from "rxjs";
import RealtimeSymbol from "../models/symbols/RealtimeSymbol";
import Env from "../env";
import WsService, {IChannel, ISubscriptionRequest, NullableSymbol} from "./WsService";

class StockService {

    private http: HttpService;
    private ws: WsService;

    private LIVE_QUOTES: string = "live_quotes";

    private _subscribedSymbolsSubject: BehaviorSubject<string[]> = new BehaviorSubject<string[]>([]);
    private _subscriptions: Subscription[] = [];
    private _liveQuoteChannel: IChannel | null = null;

    public get connected$(): Observable<boolean> {
        return this.ws.connected$;
    }
    public get connected(): boolean {
        return this.ws.connected;
    }

    public get liveQuotes$(): Observable<NullableSymbol> {
        if (this._liveQuoteChannel == null) {
            throw new Error("subscriptions to live quote stream not yet created");
        }
        return this._liveQuoteChannel.observable;
    }

    public get subscribedSymbols$(): Observable<string[]> {
        return this._subscribedSymbolsSubject.asObservable();
    }
    public get subscribedSymbols(): string[] {
        return this._subscribedSymbolsSubject.getValue();
    }

    private getSymbolEndpoint(symbol: string) {
        return this.http.baseApiEndpoint + "/stocks/" + symbol;
    }

    constructor() {
        this.http = new HttpService();
        this.ws = WsService.instance;

        this._handleLiveQuoteMessage = this._handleLiveQuoteMessage.bind(this);
        this._onHubConnected = this._onHubConnected.bind(this)

        this._subscriptions.push(
            this.ws.connected$.subscribe(this._onHubConnected)
        )
        this.ws.connect();
    }

    public subscribeToSymbol(symbolTicker: string): void {
        if (!this.subscribedSymbols.includes(symbolTicker)) {
            this._subscribedSymbolsSubject.next(
                this.subscribedSymbols.concat([symbolTicker]));
            this._liveQuoteChannel.emitter('symbol-history', symbolTicker);
            this._liveQuoteChannel.emitter('subscribe-symbol', symbolTicker);
        }
    }

    public unsubscribeFromSymbol(symbolTicker: string): void {
        if (this.subscribedSymbols.includes(symbolTicker)) {
            this._subscribedSymbolsSubject.next(
                this.subscribedSymbols.filter(symbol => symbol !== symbolTicker));
            this._liveQuoteChannel.emitter('unsubscribe-symbol', symbolTicker);
        }
    }

    private _onHubConnected(connected: boolean) {
        if (connected) {
            // subscribe to the live quotes channel
            console.log("LiveQuoteRepository::_onHubConnected - subscribing to live quotes channel");
            const channel = this.ws.subscribeToChannel({
                channelName: this.LIVE_QUOTES,
                handler: (data: any) => {
                    const jsonData = JSON.parse(data);
                    if (jsonData) {
                        this._handleLiveQuoteMessage(jsonData)
                    }
                }
            } as ISubscriptionRequest);
            this._liveQuoteChannel = channel;
            this._liveQuoteChannel.emitter('tracking');
        }
    }

    private _handleLiveQuoteMessage(message: any) {
        if (!this._liveQuoteChannel) {
            throw new Error("trying to handle a message from a channel not being tracked");
        }

        const { command } = message;

        if (command == 'live-quote') {
            const commandData = JSON.parse(message["data"]);
            for (let i = 0; i < commandData.length; i++) {
                const newSymbol = new RealtimeSymbol(commandData[i]);
                // fudge the dates so that it looks like a real time stream of data
                // instead of the chaotic mess IEX sandbox gives us
                newSymbol.date = new Date();
                this._liveQuoteChannel.subject.next(newSymbol);
            }
        }
        if (command == 'list-symbols') {
            const commandData = message["data"];
            if (commandData.length > 0) {
                for (let i = 0; i < commandData.length; i++) {
                    const symbolTicker = commandData[i];
                    if (Env.DEBUG) {
                        console.log('ClientHubRepository::_handle_live_quote_message - updating tracked list with', symbolTicker);
                    }
                    if (!this.subscribedSymbols.includes(symbolTicker)) {
                        this._subscribedSymbolsSubject.next(
                            this.subscribedSymbols.concat([symbolTicker])
                        );
                    }
                }
            } else {
                if (Env.DEBUG) {
                    console.log('ClientHubRepository::_handle_live_quote_message - upstream not tracking symbols, no-op');
                }
            }
        }
    }
}

export default StockService;