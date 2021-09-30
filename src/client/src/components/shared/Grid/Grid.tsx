import styles from "./Grid.module.scss";
import React from "react";
import {Col, Container, Row} from "react-bootstrap";

export interface IGridProps {
    children: Row[];
}

class Grid extends React.Component<IGridProps, {}> {
    render() {
        return <>
            <Container fluid className={styles.Grid}>
                { this.props.children.map(child => child) }
            </Container>
        </>
    }
}

// expose the React row and col through the Grid
// we technically don't need to do this, but it makes using the grid nicer
Grid.Row = Row;
Grid.Col = Col;

export default Grid;
