import styles from "./InvestmentAccountSummary.module.scss";
import React from "react";
import Account, {IAccount} from "../../../models/Account";
import {Col, Container, Row} from "react-bootstrap";
import HoldingsList from "../HoldingsList/HoldingsList";
import {getHoldingsState} from "../../../stores/AppStore";
import Holding, {IHolding} from "../../../models/Holding";
import BigLoader from "../../shared/Loaders/BigLoader";

export interface IInvestmentAccountSummaryProps {
    account: Account;
}

export interface IInvestmentAccountSummaryState {

}

class InvestmentAccountSummary extends React.Component<IInvestmentAccountSummaryProps, IInvestmentAccountSummaryState> {

    public get loading(): boolean {
        return this.holdings.length === 0;
    }

    public get holdings(): Holding[] {
        const holdingShapes: IHolding[] = (getHoldingsState()
            .find(accountHolding => accountHolding.accountId == this.props.account.id)
            ?.holdings) ?? [];
        const holdings = holdingShapes.map(holdingShape => new Holding(holdingShape));
        return holdings;
    }

    render() {

        if (this.loading) {
            return <BigLoader></BigLoader>
        }

        return <div className={styles.InvestmentAccountSummary}>
            <Container>
                <Row>
                    <Col>
                        <HoldingsList account={this.props.account} holdings={this.holdings} />
                    </Col>
                </Row>
            </Container>
        </div>
    }
}

export default InvestmentAccountSummary;
