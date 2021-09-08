import BaseRepository from "./BaseRepository";
import {Observable, Subject, Subscription} from "rxjs";
import ClientHubRepository, {IChannel, ISubscriptionRequest, NullableSymbol} from "./ClientHubRepository";
import Symbol from "../models/Symbol";
import Env from "../env";

class LiveQuoteRepository extends BaseRepository {

    private LIVE_QUOTES: string = "live_quotes";

    private _chRepo: ClientHubRepository | null = null;
    private _subscribedSymbols: string[] = [];
    private _subscriptions: Subscription[] = [];
    private _liveQuoteChannel: IChannel | null = null;

    public get connected$(): Observable<boolean> {
        return this._chRepo.connected$;
    }

    public get liveQuotes$(): Observable<NullableSymbol> {
        if (this._liveQuoteChannel == null) {
            throw new Error("subscriptions to live quote stream not yet created");
        }
        return this._liveQuoteChannel.observable;
    }

    public get subscribedSymbols(): string[] {
        return this._subscribedSymbols;
    }

    private static _instance: LiveQuoteRepository | null = null;
    public static get instance(): LiveQuoteRepository {
        if (!this._instance) {
            this._instance = new LiveQuoteRepository();
        }
        return this._instance;
    }

    private constructor() {
        super();

        this._handleLiveQuoteMessage = this._handleLiveQuoteMessage.bind(this);
        this._onHubConnected = this._onHubConnected.bind(this)

        this._chRepo = ClientHubRepository.instance;
        this._subscriptions.push(
            this._chRepo.connected$.subscribe(this._onHubConnected)
        )
        this._chRepo.connect();
    }


    public subscribeToSymbol(symbolTicker: string): void {
        if (!this._subscribedSymbols.includes(symbolTicker)) {
            this._subscribedSymbols.push(symbolTicker);
            this._liveQuoteChannel.emitter('symbol-history', symbolTicker);
            this._liveQuoteChannel.emitter('subscribe-symbol', symbolTicker);
        }
    }

    public unsubscribeFromSymbol(symbolTicker: string): void {
        if (this._subscribedSymbols.includes(symbolTicker)) {
            this._subscribedSymbols = this._subscribedSymbols.filter(symbol => symbol !== symbolTicker);
            this._liveQuoteChannel.emitter('unsubscribe-symbol', symbolTicker);
        }
    }

    private _onHubConnected(connected: boolean) {
        if (connected) {
            // subscribe to the live quotes channel
            console.log("LiveQuoteRepository::_onHubConnected - subscribing to live quotes channel");
            const channel = this._chRepo.subscribeToChannel({
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
                const newSymbol = new Symbol(commandData[i]);
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
                    if (!this._subscribedSymbols.includes(symbolTicker)) {
                        this._subscribedSymbols.push(symbolTicker);
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

export default LiveQuoteRepository;
