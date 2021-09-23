import styles from './HoldingsList.module.scss';
import React from "react";
import Holding, {IHolding} from "../../../models/Holding";
import {formatAsCurrency} from "../../../utilities";
import Account, {IAccount} from "../../../models/Account";
import IHistoricalEoDResponse from "../../../responses/HistoricalEoDResponse";
import HistoricalEoDSymbol, {IHistoricalEoDSymbol} from "../../../models/symbols/HistoricalEoDSymbol";
import StockService from "../../../services/StockService";
import moment from "moment";
import Env from "../../../env";

export interface IHoldingListItemProps {
    active: boolean;
    account: Account;
    holding: Holding;
}

export interface IHoldingListItemState {
    loading: boolean;
    latestPrice: HistoricalEoDSymbol;
}

class HoldingListItem extends React.Component<IHoldingListItemProps, IHoldingListItemState> {

    private stocks: StockService;

    constructor(props: IHoldingListItemProps) {
        super(props);

        this.state = {
            loading: !!this.props.holding.securitySymbol,
            latestPrice: null
        }

        this._handlePreviousPrice = this._handlePreviousPrice.bind(this);

        this.stocks = new StockService();
    }

    componentDidMount() {
        if (this.props.holding.securitySymbol) {
            this.stocks.previous(this.props.holding.securitySymbol)
                .then(this._handlePreviousPrice);
        } else {
            if (Env.DEBUG) {
                console.log("HoldingListItem::componentDidMount - not looking for symbol latest price, no symbol found");
            }
        }
    }

    componentDidUpdate(prevProps: Readonly<IHoldingListItemProps>,
                       prevState: Readonly<IHoldingListItemState>, snapshot?: any) {
        // todo - maybe add a check and fetch the price again if it's old enough?
    }

    private _handlePreviousPrice(previous: IHistoricalEoDSymbol) {
        if (previous) {
            this.setState(prev => ({
                ...prev,
                latestPrice: previous,
                loading: false
            }));
        } else {
            if (Env.DEBUG) {
                console.log("HoldingListItem::_handlePreviousPrice - price from server was undefined for ticker",
                    this.props.holding.securitySymbol);
            }
            this.setState(prev => ({
                ...prev,
                loading: false
            }));
        }
    }

    public formatQuantity(val: number): string {
        return val.toFixed(2);
    }

    public getTimestamp(): string {
        if (this.state.latestPrice) {
            return moment(this.state.latestPrice.date).utc().fromNow();
        }
        return moment(this.props.holding.timestamp).utc().fromNow();
    }

    public formatLastPrice(val: number): string {
        if (!val || val === -1) {
            return '???';
        }
        return formatAsCurrency(val);
    }

    render() {
        return <div className={styles.HoldingsListItem}>
            {
                this.state.loading && <span className={styles.HoldingListItemLoading}>
                  Updating price...
                </span>
            }
            <div>
                <p className={styles.HoldingsListItemSymbol}>
                    { this.props.holding.securitySymbol ?? '???' }
                </p>
                <span className={styles.HoldingListItemDetail}>
                    <span className={styles.HoldingListItemDetailQuantity}>
                        { this.formatQuantity(this.props.holding.quantity) }
                    </span>
                    @
                    <span className={styles.HoldingListItemDetailCost}>
                        { this.formatLastPrice(this.state.latestPrice?.close) }
                    </span>
                    each
                </span>
                <p className={styles.HoldingListItemTimestamp}>
                    { this.getTimestamp() }
                </p>
            </div>
        </div>
    }
}

export default HoldingListItem;
