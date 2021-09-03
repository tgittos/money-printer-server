import BaseRepository from "./BaseRepository";
import {io, Socket} from "socket.io-client";
import {BehaviorSubject, observable, Observable, Subject} from "rxjs";
import Env from "../env";
import {ISymbol} from "../models/Symbol";

export type NullableSymbol = ISymbol | Symbol | null;

interface IChannel {
    name: string;
    subject: BehaviorSubject<NullableSymbol>;
    observable: Observable<NullableSymbol>;
}

class ClientHubRepository extends BaseRepository {

    private LIVE_QUOTES: string = "live_quotes";

    private _ws: Socket;
    private _openedChannels: IChannel[] = [];
    private _subscribedSymbols: string[] = [];

    public get subscribedSymbols(): string[] {
        return this._subscribedSymbols;
    }

    constructor() {
        super();

        this.apiEndpoint = "symbols/"
    }

    public subscribeToSymbol(symbolTicker: string): Observable<NullableSymbol> {
        if (!this._subscribedSymbols.includes(symbolTicker)) {
            this._subscribedSymbols.push(symbolTicker);
            const { observable } = this._subscribe_to_channel(this.LIVE_QUOTES, this._subscribedSymbols);
            return observable;
        }
        const existingObservable = this._openedChannels.filter(channel => channel.name === this.LIVE_QUOTES)[0];

        if (existingObservable === undefined)
        {
            throw Error("symbol found in _subscribedSymbols, but not found in opened channels");
        }

        return existingObservable.observable;
    }

    public unsubscribeFromSymbol(symbolTicker: string) {
        if (this._subscribedSymbols.includes(symbolTicker)) {
            this._subscribedSymbols = this._subscribedSymbols.filter(symbol => symbol !== symbolTicker);
        }
        if (this._subscribedSymbols.length > 0) {
            this._subscribe_to_channel(this.LIVE_QUOTES, this._subscribedSymbols);
        } else {
            this._unsubscribe_from_channel(this.LIVE_QUOTES);
        }
    }

    public connect() {
        this._ws = io('ws://127.0.0.1:5000', { transports: ["websocket", "polling"]});
        this._ws.on('connect', this._ws_on_connect.bind(this));
        this._ws.on('reconnect', this._ws_on_reconnect.bind(this));
        this._ws.on('connect_error', this._ws_on_connect_error.bind(this));
        this._ws.on('disconnect', this._ws_on_disconnect.bind(this));
    }

    public disconnect() {
        if (this._ws.connected) {
            this._ws.disconnect();
        }
    }

    public reconnect() {
        if (this._ws.disconnected) {
            this._ws.connect();
        }
    }

    private _subscribe_to_channel(event: string, data: any): IChannel {
        if (this._openedChannels.filter(channel => channel.name == event).length > 0) {
            // already subscribed to this channel, no-op
            return;
        }

        const newSubject: BehaviorSubject<NullableSymbol> = new BehaviorSubject<NullableSymbol>(null);
        const newObservable: Observable<NullableSymbol> = newSubject.asObservable();
        if (Env.DEBUG) {
            console.log('ClientHubRepository::_subscribe_to_channel - subscribing to event:', event);
        }
        this._ws.on(event, (data: string) => {
            const json_data: ISymbol[] = JSON.parse(data);
            if (Env.DEBUG) {
                console.log(`ClientHubRepository::on_${event} received data (${json_data.length} items):`, json_data)
            }
            for (let i; i < json_data.length; i++)
            {
                if (Env.DEBUG) {
                    console.log(`ClientHubRepository::on_${event} publishing on stream subject:`, json_data[i])
                }
                newSubject.next(json_data[i]);
            }
        });
        if (Env.DEBUG) {
            console.log('ClientHubRepository::_subscribe_to_channel - emitting subscription request:', 'subscribe_' + event, data);
        }
        this._ws.emit('subscribe_' + event, data);
        const channel = {
            name: event,
            subject: newSubject,
            observable: newObservable
        } as IChannel;
        this._openedChannels.push(channel)

        return channel
    }

    private _unsubscribe_from_channel(event: string) {
        const openedChannel: IChannel[] = this._openedChannels.filter(channel => channel.name == event);
        this._openedChannels = this._openedChannels.filter(channel => channel.name !== event);

        if (openedChannel.length == 0) {
            // not subscribed in the first place, no-op
            return;
        }

        if (openedChannel.length > 1) {
            throw new Error("woah, we have more than one open channel for this event?");
        }

        const openChannel: IChannel = openedChannel[0];
        const { subject } = openChannel;
        if (Env.DEBUG) {
            console.log('ClientHubRepository::_unsubscribe_from_channel - emitting unsubscription request:', 'unsubscribe_' + event);
        }
        this._ws.emit('unsubscribe_' + event);
        if (Env.DEBUG) {
            console.log('ClientHubRepository::_unsubscribe_from_channel - unsubscribing subject');
        }
        subject.unsubscribe();
    }

    private _ws_on_connect() {
        if (Env.DEBUG) {
            console.log('ClientHubRepository::_ws_on_connect - connection to client-hub established');
        }
    }

    private _ws_on_disconnect() {
        if (Env.DEBUG) {
            console.log('ClientHubRepository::_ws_on_disconnect - disconnected from client-hub');
        }
    }

    private _ws_on_connect_error() {
        if (Env.DEBUG) {
            console.log('ClientHubRepository::_ws_on_connect_error - error establishing connection');
        }
    }

    private _ws_on_reconnect() {
        if (Env.DEBUG) {
            console.log('SymbolRepository::_ws_on_reconnect - reconnected to client-hub');
        }
    }
}

export default ClientHubRepository;
