import styles from "./Grid.module.scss";
import React, {ElementType, ReactNode} from "react";
import {Col, Container, Row} from "react-bootstrap";

export interface IGridProps {
    children: React.ReactNode;
    className?: string;
}

const Grid = (props: IGridProps) => {
    const { className } = props;
    const classes = [
        styles.Grid,
        'mp-grid',
        className
    ]

    return <>
        <Container className={classes.join(' ')} {...props} />
    </>
}
Grid.Row = Row;
Grid.Col = Col;

export default Grid;
