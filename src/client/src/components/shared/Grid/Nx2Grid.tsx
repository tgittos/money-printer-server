import styles from "./Grid.module.scss";
import React from "react";
import {Col, Container} from "react-bootstrap";
import Nx2Row from "./Nx2Row";

export interface IGridProps {
    children: Nx2Row[];
}

class Nx2Grid extends React.Component<IGridProps, {}> {
    static Row = Nx2Row;
    static Col = Col;

    render() {
        return <>
            <Container fluid className={styles.Grid}>
                { this.props.children.map(child => child) }
            </Container>
        </>
    }
}


export default Nx2Grid;
