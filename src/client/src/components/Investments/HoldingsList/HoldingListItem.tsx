import styles from './HoldingsList.module.scss';
import React from "react";
import Holding, {IHolding} from "../../../models/Holding";
import {formatAsCurrency} from "../../../utilities";
import Account, {IAccount} from "../../../models/Account";
import IHistoricalEoDResponse from "../../../responses/HistoricalEoDResponse";
import HistoricalEoDSymbol from "../../../models/symbols/HistoricalEoDSymbol";
import StockService from "../../../services/StockService";
import moment from "moment";

export interface IHoldingListItemProps {
    active: boolean;
    account: Account;
    holding: Holding;
    latestPrice: number;
}

export interface IHoldingListItemState {
    previousPrice: number;
}

class HoldingListItem extends React.Component<IHoldingListItemProps, IHoldingListItemState> {

    private stocks: StockService;

    constructor(props: IHoldingListItemProps) {
        super(props);

        this._handlePreviousPrice = this._handlePreviousPrice.bind(this);

        this.stocks = new StockService();
    }

    componentDidMount() {
    }

    private _handlePreviousPrice(previous: HistoricalEoDSymbol) {
        this.setState(prev => ({
            ...prev,
            previousPrice: previous.close
        }));
    }

    public formatQuantity(val: number): string {
        return val.toFixed(2);
    }

    public formatTimestamp(val: Date): string {
        return moment(val).fromNow();
    }

    public formatLastPrice(val: number): string {
        if (!val || val === -1) {
            return '???';
        }
        return formatAsCurrency(val);
    }

    render() {
        return <div className={styles.HoldingsListItem}>
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
                        { this.formatLastPrice(this.props.latestPrice) }
                    </span>
                    each
                </span>
                <p className={styles.HoldingListItemTimestamp}>
                    { this.formatTimestamp(this.props.holding.timestamp) }
                </p>
            </div>
        </div>
    }
}

export default HoldingListItem;
