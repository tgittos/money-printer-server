import React from 'react';
import styles from './SymbolTracker.module.scss';
import { IProfile } from "../../models/Profile";
import ClientHubRepository, { NullableSymbol } from "../../repositories/ClientHubRepository";
import Env from "../../env";
import {Observable, Subscription} from "rxjs";
import {CloseButton, ListGroup} from "react-bootstrap";

interface ISymbolTrackerProps {
}

interface ISymbolTrackerState {
    profile: IProfile,
    subscribedSymbols: string[],
    newSymbol: string;
}

class SymbolTracker extends React.Component<ISymbolTrackerProps, ISymbolTrackerState> {

    private _clientHubRepo: ClientHubRepository;
    private _liveData: Subscription;

    public get subscribedSymbols(): string[] {
        return this._clientHubRepo.subscribedSymbols;
    }

    constructor(props: ISymbolTrackerProps) {
        super(props);

        this.handleSubscribe = this.handleSubscribe.bind(this);
        this.handleUnsubscribe = this.handleUnsubscribe.bind(this);

        this._clientHubRepo = new ClientHubRepository();

        this.state = {
            profile: props.profile,
            subscribedSymbols: this.subscribedSymbols,
        } as ISymbolTrackerState;
    }

    componentDidMount() {
        this._clientHubRepo.connect();
        if (Env.DEBUG) {
            console.log('SymbolTracker::componentDidMount - subscribing to live quotes');
        }
        /*
        this._liveData = this._clientHubRepo.liveQuotes$.subscribe(symbol => {
            console.log('SymbolTracker::liveQuote listener - got data:', symbol);
        });
         */
    }

    componentWillUnmount() {
        // this._liveData?.unsubscribe();
        this._clientHubRepo.disconnect();
    }

    private handleSubscribe(symbol: string) {
        if (Env.DEBUG) {
            console.log('SymbolTracker::handleSubscribe - subscribing to', this.state.newSymbol);
        }

        this._clientHubRepo.subscribeToSymbol(symbol);

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

        this._clientHubRepo.unsubscribeFromSymbol(symbol);

        this.setState((prev: ISymbolTrackerState) => {
            const { subscribedSymbols } = prev;
            return {
                ...prev,
                newSymbol: '',
                subscribedSymbols: subscribedSymbols.filter(s => s !== symbol)
            }
        });
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
