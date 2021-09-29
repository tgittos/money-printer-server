import styles from "./InvestmentAccountSummary.module.scss";
import React from "react";
import moment from "moment";
import Account, {IAccount} from "../../../models/Account";
import {Col, Container, Row} from "react-bootstrap";
import HoldingsList from "../HoldingsList/HoldingsList";
import {getHoldingsState} from "../../../stores/AppStore";
import Holding, {IHolding} from "../../../models/Holding";
import BigLoader from "../../shared/Loaders/BigLoader";
import BasicCandleChart from "../../Charts/lib/charts/BasicCandleChart";
import LiveChart from "../../Charts/LiveChart";
import StaticChart from "../../Charts/StaticChart";
import PieChart from "../../Charts/lib/charts/PieChart";
import {IPieData} from "../../Charts/lib/figures/Pie";
import IChartDimensions from "../../Charts/interfaces/IChartDimensions";
import InvestmentPerformance from "../InvestmentPerformance/InvestmentPerformance";

export interface IInvestmentAccountSummaryProps {
    account: Account;
}

export interface IInvestmentAccountSummaryState {
    activeHolding: Holding | null;
}

class InvestmentAccountSummary extends React.Component<IInvestmentAccountSummaryProps, IInvestmentAccountSummaryState> {

    public get loading(): boolean {
        return this.holdings.length === 0;
    }

    public get activeHolding(): Holding | null {
        return this.state.activeHolding;
    }

    public get holdings(): Holding[] {
        const holdingShapes: IHolding[] = (getHoldingsState()
            .find(accountHolding => accountHolding.accountId == this.props.account.id)
            ?.holdings) ?? [];
        const holdings = holdingShapes.map(holdingShape => new Holding(holdingShape));
        return holdings;
    }

    constructor(props: IInvestmentAccountSummaryProps) {
        super(props);

        this.state = {
            activeHolding: null
        }

        this._onActiveHoldingChanged = this._onActiveHoldingChanged.bind(this);
    }

    private _onActiveHoldingChanged(holding: Holding) {
        this.setState(prev => ({
            ...prev,
            activeHolding: holding
        }));
    }

    private get chartDimensions(): IChartDimensions {
        return {
            width: 1000,
            height: 600,
            margin: {
                top: 10,
                left: 10,
                right: 10,
                bottom: 10
            }
        } as IChartDimensions;
    }

    private get pieChartData(): IPieData[] {
        return this.holdings.map(holding => ({
            name: holding.securitySymbol ?? '???',
            value: holding.quantity * holding.latestPrice
        } as IPieData));
    }

    render() {

        if (this.loading) {
            return <BigLoader></BigLoader>
        }

        return <div className={styles.InvestmentAccountSummary}>
            <Container fluid>
                <Row>
                    <Col xs={2}>
                        <HoldingsList onActiveChanged={this._onActiveHoldingChanged}
                                      account={this.props.account}
                                      holdings={this.holdings} />
                    </Col>
                    <Col>
                        {
                            this.activeHolding
                                ? <InvestmentPerformance holding={this.activeHolding}/>
                                : (<div>
                                        <div className={styles.InvestmentAccountSummaryHeader}>
                                            <Container>
                                                <Row>
                                                    <Col>
                                                        { this.props.account.name }
                                                    </Col>
                                                    <Col>
                                                        { this.props.account.type} ({this.props.account.subtype})
                                                    </Col>
                                                    <Col>
                                                        Balance: { this.props.account.balance }
                                                    </Col>
                                                    <Col>
                                                        Performance: TODO
                                                    </Col>
                                                    <Col>
                                                        Last updated: { moment.utc(this.props.account.timestamp).fromNow() }
                                                    </Col>
                                                </Row>
                                            </Container>
                                        </div>
                                        <StaticChart chart={PieChart}
                                                   dimensions={this.chartDimensions}
                                                   data={this.pieChartData}
                                                   labelFormatter={datum => datum.name}
                                                   />
                                    </div>)
                        }
                    </Col>
                </Row>
            </Container>
        </div>
    }
}

export default InvestmentAccountSummary;
