import styles from "../Header.module.scss";
import {formatAsCurrency} from "../../../../lib/Utilities";
import {MdTrendingUp, MdTrendingDown, MdTrendingFlat} from "react-icons/all";
import {Col, Row} from "react-bootstrap";
import Grid from "../../../shared/Grid/Grid";

export interface IMarketTrackerProps {

}

interface IMarketTrackerItemProps {
    ticker: string;
    label?: string;
    price: number;
    changePrice: number;
    changePct: number;
}

const MarketTrackerItem = (props: IMarketTrackerItemProps) => {
    const trendClass = props.changePct > 0
        ? "gain"
        : props.changePct < 0
            ? "loss"
            : "flat";

    const classes = [
        styles.MarketTrackerItem,
        "mp-market-tracker-item",
        trendClass
    ]

    const changeIcon = trendClass === "gain"
        ? <MdTrendingUp />
        : trendClass === "loss"
            ? <MdTrendingDown />
            : <MdTrendingFlat />


    return <Grid className={classes.join(' ')}>
        <Row className="mp-ticker">
            <Col>
                <span>{ props.label ?? props.ticker }</span>
                <span className="mp-trend-icon">{ changeIcon }</span>
            </Col>
        </Row>
        <Row className="mp-ticker-price">
            <span>{ formatAsCurrency(props.price) }</span>
        </Row>
        <Row className="mp-ticker-change">
            <Col className="mp-price">
                { formatAsCurrency(props.changePrice) }
            </Col>
            <Col className="mp-percent">
                ({ props.changePct }%)
            </Col>
        </Row>
    </Grid>
}

const MarketTracker = (props: IMarketTrackerProps) => {
    const classes = [
        styles.MarketTracker,
        'mp-market-tracker'
    ];

    return <div className={classes.join(' ')}>
        <MarketTrackerItem
            label="S&P 500"
            ticker="SPY"
            price={500.0}
            changePrice={50.0}
            changePct={0.1}
        />
        <MarketTrackerItem
            label="NASDAQ"
            ticker=".IXIC"
            price={15000}
            changePrice={-50.0}
            changePct={-0.1}
        />
        <MarketTrackerItem
            label="Dow Jones"
            ticker="DJI"
            price={30000}
            changePrice={0}
            changePct={0}
        />
    </div>;
}

export default MarketTracker;
