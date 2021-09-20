import styles from './HoldingsList.module.scss';
import React from "react";
import HoldingListItem from "./HoldingListItem";
import Account, {IAccount} from "../../../models/Account";
import Holding from "../../../models/Holding";
import StockService from "../../../services/StockService";
import BigLoader from "../../shared/Loaders/BigLoader";


export interface IHoldingsListProps {
    account: Account;
    holdings: Holding[];
    onActiveChanged?: (holding: Holding) => void;
}

export interface IHoldingsListState {
    activeHoldingId: number;
}

class HoldingsList extends React.Component<IHoldingsListProps, IHoldingsListState> {

    public get activeHolding(): number {
        return this.state.activeHoldingId;
    }

    constructor(props: IHoldingsListProps) {
        super(props);

        const firstHolding = this.props.holdings[0]?.id ?? 0;

        this.state = {
            activeHoldingId: firstHolding,
        }

        this._onHoldingClicked = this._onHoldingClicked.bind(this);
    }

    componentDidMount() {
    }

    private _onHoldingClicked(holdingId: number) {
       const holding = this.props.holdings.find(holding => holding.id === holdingId);
       if (holding) {
           this.setState(prev => ({
               ...prev,
               activeHoldingId: holdingId
           }));
           if (this.props.onActiveChanged) {
               this.props.onActiveChanged(holding);
           }
       }
    }

    render() {
        return <div className={styles.HoldingsList}>
            {
                (this.props.holdings || []).map(holding =>
                    <div key={holding.id} onClick={() => this._onHoldingClicked(holding.id)}>
                        <HoldingListItem active={this.state.activeHoldingId === holding.id}
                                         account={this.props.account}
                                         holding={holding}
                        />
                    </div>
            )}
        </div>
    }
}

export default HoldingsList;