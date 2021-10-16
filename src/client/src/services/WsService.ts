import {io, Socket} from "socket.io-client";
import {BehaviorSubject, Observable, ReplaySubject} from "rxjs";
import Env from "../env";
import ISymbol from "../interfaces/ISymbol";

export type NullableSymbol = ISymbol | null;
type NullableChannel = IChannel | null;

export interface IChannel {
    name: string;
    subject: ReplaySubject<NullableSymbol>;
    observable: Observable<NullableSymbol>;
    emitter: (message: string, data?: any) => void,
}

export interface ISubscriptionRequest {
    channelName: string;
    handler: (data: any) => void,
    data: any
}

class WsService {


    private MESSAGE_BUFFER_SIZE: number = 1000;

    private _connected: boolean;
    private _ws: Socket;
    private _openedChannels: IChannel[] = [];
    private _connectionStateSubject: BehaviorSubject<boolean> = new BehaviorSubject<boolean>(false);
    private _connectionStateObservable: Observable<boolean> = this._connectionStateSubject.asObservable();
    private _connectFailureCount: number = 0;

    public get connected$(): Observable<boolean> {
        return this._connectionStateObservable;
    }
    public get connected(): boolean {
        return this._connectionStateSubject.getValue();
    }

    private static _instance: WsService;
    public static get instance(): WsService {
        if (!this._instance) {
            this._instance = new WsService();
        }
        return this._instance;
    }

    private constructor() {
    }

    public connect() {
        if (!this._connected) {
            this._ws = io('ws://127.0.0.1:5000', {transports: ["websocket", "polling"]});
            this._ws.on('connect', this._ws_on_connect.bind(this));
            this._ws.on('reconnect', this._ws_on_reconnect.bind(this));
            this._ws.on('connect_error', this._ws_on_connect_error.bind(this));
            this._ws.on('disconnect', this._ws_on_disconnect.bind(this));
            this._ws.on('close', this._ws_on_close.bind(this));
        }
    }

    public disconnect() {
        if (this._ws.connected) {
            this._ws.disconnect();
            this._connected = false;
            this._connectionStateSubject.next(this._connected);
        }
    }

    public reconnect() {
        if (this._ws.disconnected) {
            this._ws.connect();
        }
    }

    public subscribeToChannel(request: ISubscriptionRequest): IChannel {
        const { channelName, data, handler } = request;
        if (!this._connected) {
            this.connect();
        }
        const existingChannel = this.getChannel(channelName);
        if (existingChannel != null) {
            return existingChannel;
        }

        const newSubject: ReplaySubject<NullableSymbol> = new ReplaySubject<NullableSymbol>(this.MESSAGE_BUFFER_SIZE);
        const newObservable: Observable<NullableSymbol> = newSubject.asObservable();
        if (Env.DEBUG) {
            console.log('ClientHubRepository::_subscribe_to_channel - subscribing to channel:', channelName);
        }
        this._ws.on(channelName, handler);
        if (Env.DEBUG) {
            console.log('ClientHubRepository::_subscribe_to_channel - emitting subscription request:', 'subscribe_' + channelName);
        }
        this._ws.emit('subscribe_' + channelName, data);
        const channel = {
            name: channelName,
            subject: newSubject,
            observable: newObservable,
            emitter: (message: string, data: any = null) => {
                this._messageSubscribedChannel(channelName, message, data);
            }
        } as IChannel;
        this._openedChannels.push(channel)

        return channel
    }

    public unsubscribeFromChannel(channelName: string) {
        const openChannel = this.getChannel(channelName);
        if (openChannel == null) {
            return;
        }

        this._openedChannels = this._openedChannels.filter(channel => channel.name !== channelName);

        if (!this._connected) {
            return;
        }

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

    public getChannel(channelName: string): NullableChannel {
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

    private _isSubscribedToChannel(channelName: string): boolean {
        const openedChannel: IChannel[] = this._openedChannels.filter(channel => channel.name == channelName);
        return openedChannel.length > 0;
    }

    private _messageSubscribedChannel(channelName: string, message: string, data: any = null) {
        if (!this._connected) {
            this.connect();
        }

        const openedChannel = this.getChannel(channelName);

        if (openedChannel == null) {
            // trying to send a message to a channel we haven't subscribed to
            throw new Error("trying to send a message to an unopened channel");
        }

        this._message_unsubscribed_channel(channelName, message, data);
    }

    private _message_unsubscribed_channel(channelName: string, message: string, data: any = null) {
        if (data == null) {
            if (Env.DEBUG) {
                console.log(`ClientHubRepository::_message_channel - sending ${channelName}:${message}`);
            }
            this._ws.emit(`${channelName}:${message}`);
        } else {
            if (Env.DEBUG) {
                console.log(`ClientHubRepository::_message_channel - sending ${channelName}:${message} with data:`, data);
            }
            this._ws.emit(`${channelName}:${message}`, data);
        }
    }

    private _ws_on_connect() {
        if (Env.DEBUG) {
            console.log('ClientHubRepository::_ws_on_connect - connection to client-hub established');
        }

        this._connectFailureCount = 0;
        this._connected = true;
        this._connectionStateSubject.next(this._connected);
    }

    private _ws_on_disconnect() {
        if (Env.DEBUG) {
            console.log('ClientHubRepository::_ws_on_disconnect - disconnected from client-hub');
        }

        this._connectFailureCount = 0;
        this._connected = false;
        this._connectionStateSubject.next(this._connected);
    }

    private _ws_on_connect_error() {
        if (Env.DEBUG) {
            console.log('ClientHubRepository::_ws_on_connect_error - error establishing connection, retry count:', 5 - this._connectFailureCount);
        }
        this._connectFailureCount += 1;

        if (this._connectFailureCount > 5) {
            // give up, it ain't happening for some reason
            if (Env.DEBUG) {
                console.log('ClientHubRepository::_ws_on_connect_error - giving up on connecting');
            }
            this._ws.disconnect();
            this._ws = null;
            this._connected = false;
            this._connectionStateSubject.next(this._connected);
        }
    }

    private _ws_on_reconnect() {
        if (Env.DEBUG) {
            console.log('SymbolRepository::_ws_on_reconnect - reconnected to client-hub');
        }

        for (let i = 0; i < this._openedChannels.length; i++) {
            const channel = this._openedChannels[i];

            if (Env.DEBUG) {
                console.log('SymbolRepository::_ws_on_reconnect - resubscribing to channel', channel);
            }
            this._ws.emit('subscribe_' + channel.name);
        }

        this._connectFailureCount = 0;
        this._connected = true;
        this._connectionStateSubject.next(this._connected);
    }

    private _ws_on_close() {
        if (Env.DEBUG) {
            console.log('SymbolRepository::_ws_on_close - closing connection to client-hub');
        }
    }

}

export default WsService;