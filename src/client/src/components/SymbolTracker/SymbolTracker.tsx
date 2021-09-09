import React from 'react';
import styles from './SymbolTracker.module.scss';
import { IProfile } from "../../models/Profile";
import ClientHubRepository, { NullableSymbol } from "../../repositories/ClientHubRepository";
import Env from "../../env";
import {filter, Observable, ObservedValueOf, Subscription} from "rxjs";
import {CloseButton, ListGroup} from "react-bootstrap";
import LiveQuoteRepository from "../../repositories/LiveQuoteRepository";

interface ISymbolTrackerProps {
}

interface ISymbolTrackerState {
    profile: IProfile,
    subscribedSymbols: string[],
    newSymbol: string;
}

class SymbolTracker extends React.Component<ISymbolTrackerProps, ISymbolTrackerState> {

    private _liveQuotes: LiveQuoteRepository;
    private _subscriptions: Subscription[] = [];

    public get subscribedSymbols(): string[] {
        return this.state.subscribedSymbols;
    }

    constructor(props: ISymbolTrackerProps) {
        super(props);

        this.handleSubscribe = this.handleSubscribe.bind(this);
        this.handleUnsubscribe = this.handleUnsubscribe.bind(this);
        this.handleSymbolData = this.handleSymbolData.bind(this);
        this.handleSubscribedSymbolsUpdate = this.handleSubscribedSymbolsUpdate.bind(this);

        this._liveQuotes = LiveQuoteRepository.instance;

        this.state = {
            profile: props.profile,
            subscribedSymbols: [],
        } as ISymbolTrackerState;
    }

    componentDidMount() {
        this._subscriptions.push(
            this._liveQuotes.subscribedSymbols$.subscribe(this.handleSubscribedSymbolsUpdate)
        );
    }

    componentWillUnmount() {
    }

    private handleSubscribedSymbolsUpdate(symbols: string[]) {
        console.log('got subscribed symbols:', symbols);
        this.setState(prev => ({
            ...prev,
            subscribedSymbols: [].concat(symbols)
        }))
    }

    private handleSubscribe(symbol: string) {
        if (Env.DEBUG) {
            console.log('SymbolTracker::handleSubscribe - subscribing to', this.state.newSymbol);
        }

        this._liveQuotes.subscribeToSymbol(symbol);

        this.setState((prev: ISymbolTrackerState) => {
            const { subscribedSymbols } = prev;
            return {
                ...prev,
                newSymbol: '',
                subscribedSymbols: [].concat(subscribedSymbols).concat(symbol)
            };
        });
    }

    private handleUnsubscribe(symbol: string) {
        if (Env.DEBUG) {
            console.log('Dashboard::handleUnsubscribe - unsubscribing from symbol:', symbol);
        }

        this._liveQuotes.unsubscribeFromSymbol(symbol);

        this.setState((prev: ISymbolTrackerState) => {
            const { subscribedSymbols } = prev;
            return {
                ...prev,
                newSymbol: '',
                subscribedSymbols: subscribedSymbols.filter(s => s !== symbol)
            }
        });
    }

    private handleSymbolData(data: any) {
        console.log('got data:', data);
    }

    render() {
        const symbolListItems = this.subscribedSymbols.map((symbol) =>
            <ListGroup.Item key={symbol}>
                <span>{symbol}</span>
                <CloseButton onClick={() => this.handleUnsubscribe(symbol)}/>
            </ListGroup.Item>);

        return <div className={styles.SymbolTracker}>
            <h2>Subscribed symbols:</h2>
            <ListGroup horizontal className={styles.SymbolChipList}>
                {symbolListItems}
            </ListGroup>
            <input placeholder="SPY"
                value={this.state.newSymbol}
                onChange={(event) => this.setState(prev => ({
                    ...prev,
                    newSymbol: event.target?.value ?? ''
                }))}/>
            <button onClick={() => this.handleSubscribe(this.state.newSymbol)}>
                Add to subscriptions
            </button>
        </div>
    }
};

export default SymbolTracker;
