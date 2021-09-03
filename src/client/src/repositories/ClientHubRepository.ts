import BaseRepository from "./BaseRepository";
import {io, Socket} from "socket.io-client";
import {BehaviorSubject, observable, Observable, Subject} from "rxjs";
import Env from "../env";
import {ISymbol} from "../models/Symbol";

export type NullableSymbol = ISymbol | Symbol | null;
type NullableChannel = IChannel | null;

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

    public get liveQuotes$(): Observable<NullableSymbol> {
        let channel = this._get_channel(this.LIVE_QUOTES);
        if (channel == null) {
            channel = this._subscribe_to_channel(this.LIVE_QUOTES);
        }
        return channel.observable;
    }

    constructor() {
        super();

        this.apiEndpoint = "symbols/"
    }

    public subscribeToSymbol(symbolTicker: string): void {
        if (!this._subscribedSymbols.includes(symbolTicker)) {
            this._subscribedSymbols.push(symbolTicker);
            this._message_channel(this.LIVE_QUOTES, 'subscribe-symbol', symbolTicker);
        }
    }

    public unsubscribeFromSymbol(symbolTicker: string): void {
        if (this._subscribedSymbols.includes(symbolTicker)) {
            this._subscribedSymbols = this._subscribedSymbols.filter(symbol => symbol !== symbolTicker);
            this._message_channel(this.LIVE_QUOTES, 'unsubscribe-symbol', symbolTicker);
        }
    }

    public connect() {
        this._ws = io('ws://127.0.0.1:5000', { transports: ["websocket", "polling"]});
        this._ws.on('connect', this._ws_on_connect.bind(this));
        this._ws.on('reconnect', this._ws_on_reconnect.bind(this));
        this._ws.on('connect_error', this._ws_on_connect_error.bind(this));
        this._ws.on('disconnect', this._ws_on_disconnect.bind(this));

        // subscribe to the live quotes channel
        this._subscribe_to_channel(this.LIVE_QUOTES);
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

    private _subscribe_to_channel(channelName: string, data: any = null): IChannel {
        const existingChannel = this._get_channel(channelName);
        if (existingChannel != null) {
            return existingChannel;
        }

        const newSubject: BehaviorSubject<NullableSymbol> = new BehaviorSubject<NullableSymbol>(null);
        const newObservable: Observable<NullableSymbol> = newSubject.asObservable();
        if (Env.DEBUG) {
            console.log('ClientHubRepository::_subscribe_to_channel - subscribing to channel:', channelName);
        }
        this._ws.on(channelName, (data: string) => {
            const json_data = JSON.parse(data);
            for (let i = 0; i < json_data.length; i++)
            {
                newSubject.next(json_data[i]);
            }
        });
        if (Env.DEBUG) {
            console.log('ClientHubRepository::_subscribe_to_channel - emitting subscription request:', 'subscribe_' + channelName, data);
        }
        this._ws.emit('subscribe_' + channelName, data);
        const channel = {
            name: channelName,
            subject: newSubject,
            observable: newObservable
        } as IChannel;
        this._openedChannels.push(channel)

        return channel
    }

    private _unsubscribe_from_channel(channelName: string) {
        const openChannel = this._get_channel(channelName);
        if (openChannel == null) {
            return;
        }

        this._openedChannels = this._openedChannels.filter(channel => channel.name !== channelName);

        const { subject } = openChannel;
        if (Env.DEBUG) {
            console.log('ClientHubRepository::_unsubscribe_from_channel - emitting unsubscription request:', 'unsubscribe_' + channelName);
        }
        this._ws.emit('unsubscribe_' + channelName);
        if (Env.DEBUG) {
            console.log('ClientHubRepository::_unsubscribe_from_channel - unsubscribing subject');
        }
        subject.unsubscribe();
    }

    private _get_channel(channelName: string): NullableChannel {
        const openedChannel: IChannel[] = this._openedChannels.filter(channel => channel.name == channelName);

        if (openedChannel.length == 0) {
            // not subscribed in the first place, no-op
            return null;
        }

        if (openedChannel.length > 1) {
            throw new Error("woah, we have more than one IChannel for this channel?");
        }

        const openChannel: IChannel = openedChannel[0];
        return openChannel;
    }

    private _is_subscribed_to_channel(channelName: string): boolean {
        const openedChannel: IChannel[] = this._openedChannels.filter(channel => channel.name == channelName);
        return openedChannel.length > 0;
    }

    private _message_channel(channelName: string, message: string, data: any) {
        const openedChannel = this._get_channel(channelName);

        if (openedChannel == null) {
            // trying to send a message to a channel we haven't subscribed to
            throw new Error("trying to send a message to an unopened channel");
        }

        if (Env.DEBUG) {
            console.log(`ClientHubRepository::_message_channel - sending ${channelName}:${message} with data:`, data);
        }
        this._ws.emit(`${channelName}:${message}`, data);
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
