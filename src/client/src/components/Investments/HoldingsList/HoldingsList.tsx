import styles from './HoldingsList.module.scss';
import React from "react";
import {IAccountHolding} from "../../../slices/AccountSlice";
import HoldingListItem from "./HoldingListItem";
import Account, {IAccount} from "../../../models/Account";
import Holding from "../../../models/Holding";
import {Promise as BluebirdPromise} from "bluebird";
import HttpService from "../../../services/HttpService";
import StockService from "../../../services/StockService";
import IHistoricalEoDResponse from "../../../responses/HistoricalEoDResponse";
import {IServerHistoricalEoDSymbol} from "../../../models/symbols/HistoricalEoDSymbol";
import BigLoader from "../../shared/Loaders/BigLoader";


interface IHoldingLatestPrice {
    holdingId: number;
    previous: IServerHistoricalEoDSymbol;
}

export interface IHoldingsListProps {
    account: Account;
    holdings: Holding[];
}

export interface IHoldingsListState {
    loading: boolean;
    activeHoldingId: number;
    holdingPrices: IHoldingLatestPrice[];
}

class HoldingsList extends React.Component<IHoldingsListProps, IHoldingsListState> {

    private _stocks: StockService;

    public get activeHolding(): number {
        return this.state.activeHoldingId;
    }

    constructor(props: IHoldingsListProps) {
        super(props);

        const firstHolding = this.props.holdings[0]?.id ?? 0;

        this.state = {
            loading: true,
            activeHoldingId: firstHolding,
            holdingPrices: []
        }

        this._stocks = new StockService();

        this._onHoldingLatestFetched = this._onHoldingLatestFetched.bind(this);

    }

    componentDidMount() {
        this.fetchHoldingPrices();
    }

    private fetchHoldingPrices() {
        if ((this.props.holdings || []).length == 0) {
            console.log('not fetching prices, no holdings');
            this.setState(prev => ({
                ...prev,
                loading: false
            }));
        }
        // pull the latest price from the server for each holding
        // and pass it in to the list item
        BluebirdPromise.props(this.props.holdings.reduce((memo, holding) => {
            if (holding.securitySymbol === undefined ||
                holding.securitySymbol === null ||
                holding.securitySymbol === '') {
                return memo;
            }
            const p = this._stocks.previous(holding.securitySymbol);
            return {
                ...memo,
                [holding.id]: p
            };
        }, {})).then(this._onHoldingLatestFetched);
    }

    private _onHoldingLatestFetched(latestPrices: any) {
        const holdingPrices = this.props.holdings.map(holding => {
            const latestPrice = latestPrices[holding.id];
            if (latestPrice !== undefined) {
                return {
                    holdingId: holding.id,
                    previous: latestPrice
                } as IHoldingLatestPrice
            }
        }).filter(v => !!v);

        this.setState(prev => ({
            ...prev,
            loading: false,
            holdingPrices
        }));
    }

    private getLatestPrice(holdingId: number) {
        const { holdingPrices } = this.state;
        const holding = holdingPrices.find(holdingPrice => holdingPrice.holdingId === holdingId);
        if (holding) {
            return holding.previous?.close ?? -1;
        }
        return -1;
    }

    render() {
        if (this.state.loading) {
            return <BigLoader></BigLoader>
        }

        return <div className={styles.HoldingsList}>
            {
                (this.props.holdings || []).map(holding =>
                    <div key={holding.id}>
                        <HoldingListItem active={this.state.activeHoldingId === holding.id}
                                         account={this.props.account}
                                         holding={holding}
                                         latestPrice={this.getLatestPrice(holding.id)}
                        />
                    </div>
            )}
        </div>
    }
}

export default HoldingsList;