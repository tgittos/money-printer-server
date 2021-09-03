import React from 'react';
import styles from './Dashboard.module.scss';
import BigLoader from "../shared/Loaders/BigLoader";
import Header from "../Header/Header";
import { IProfile } from "../../models/Profile";
import MultiLineChart from "../Charts/MultiLineChart/MultiLineChart";
import ClientHubRepository, { NullableSymbol } from "../../repositories/ClientHubRepository";
import Env from "../../env";
import {Observable, Subscription} from "rxjs";

interface IDashboardProps {
    profile: IProfile
}

interface IDashboardState {
    profile: IProfile,
    subscribedSymbols: string[],
    newSymbol: string;
}

class Dashboard extends React.Component<IDashboardProps, IDashboardState> {

    private _clientHubRepo: ClientHubRepository;
    private _liveData: Subscription;

    public get subscribedSymbols(): string[] {
        return this._clientHubRepo.subscribedSymbols;
    }

    constructor(props: IDashboardProps) {
        super(props);

        this.handleSubscribe = this.handleSubscribe.bind(this);
        this.handleUnsubscribe = this.handleUnsubscribe.bind(this);

        this._clientHubRepo = new ClientHubRepository();

        this.state = {
            profile: props.profile,
            subscribedSymbols: this.subscribedSymbols,
        } as IDashboardState;
    }

    componentDidMount() {
        this._clientHubRepo.connect();
    }

    componentWillUnmount() {
        this._liveData?.unsubscribe();
        this._clientHubRepo.disconnect();
    }

    private handleSubscribe() {
        if (Env.DEBUG) {
            console.log('Dashboard::handleSubscribe - subscribing to', this.state.newSymbol);
        }

        const observable: Observable<NullableSymbol> =
            this._clientHubRepo.subscribeToSymbol(this.state.newSymbol);
        this._liveData = observable.subscribe((data) => data && console.log(data));
        this.setState((prev: IDashboardState) => {
            const { newSymbol, subscribedSymbols } = prev;
            return {
                ...prev,
                newSymbol: '',
                subscribedSymbols: [].concat(subscribedSymbols).concat(newSymbol)
            };
        });
    }

    private handleUnsubscribe() {
        if (Env.DEBUG) {
            console.log('Dashboard::handleUnsubscribe - unsubscribing from all symbols');
        }

        this._liveData?.unsubscribe();
        this.state.subscribedSymbols.forEach(symbol =>
            this._clientHubRepo.unsubscribeFromSymbol(symbol));
        this.setState((prev: IDashboardState) => {
            const { subscribedSymbols } = prev;
            return {
                ...prev,
                newSymbol: '',
                subscribedSymbols: []
            }
        });
    }

    render() {
        return <div className={styles.Dashboard}>
            <Header profile={this.state.profile}></Header>
            <div>
                <h2>Subscribed symbols:</h2>
                <p>{this.subscribedSymbols.length > 0
                    ? this.subscribedSymbols.join(', ')
                    : 'None'}</p>
                <div>
                    <input placeholder="SPY"
                        value={this.state.newSymbol}
                        onChange={(event) => this.setState(prev => ({
                            ...prev,
                            newSymbol: event.target?.value ?? ''
                        }))}/>
                    <button onClick={this.handleSubscribe}>
                        Add to subscriptions
                    </button>
                </div>
                <button onClick={this.handleUnsubscribe}>Unsubscribe all</button>
            </div>
            <MultiLineChart></MultiLineChart>
        </div>
    }
};

export default Dashboard;
