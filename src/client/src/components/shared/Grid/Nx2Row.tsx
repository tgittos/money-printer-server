import styles from "./Grid.module.scss";
import React from "react";
import {Col, Row} from "react-bootstrap";

export interface INx2RowProps {
    children: Col[];
}

class Nx2Row extends React.Component<INx2RowProps, {}> {
    render() {
        if ((this.props.children?.length ?? 0) > 2) {
            throw Error("Nx2Row only accepts at most 2 Col children");
        }

        return <>
            <Row className={styles.Row}>
                { this.props.children.map(child => child) }
            </Row>
        </>
    }
}

Nx2Row.Col = Col;

export default Nx2Row;
