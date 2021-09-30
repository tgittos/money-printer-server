import styles from "./Grid.module.scss";
import React from "react";
import {Col, Container} from "react-bootstrap";
import Nx2Row from "./Nx2Row";

export interface IGridProps {
    children: Nx2Row[];
}

class Nx2Grid extends React.Component<IGridProps, {}> {
    render() {
        return <>
            <Container fluid className={styles.Grid}>
                { this.props.children.map(child => child) }
            </Container>
        </>
    }
}

Nx2Grid.Row = Nx2Row;
Nx2Grid.Col = Col;

export default Nx2Grid;
