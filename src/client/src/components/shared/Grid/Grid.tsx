import styles from "./Grid.module.scss";
import React from "react";
import {Col, Container, Row} from "react-bootstrap";

export interface IGridProps extends React.ComponentPropsWithoutRef<HTMLDivElement>{
    children: Row[];
}

class Grid extends React.Component<IGridProps, {}> {
    static Row = Row;
    static Col = Col;

    render() {
        const { className } = this.props;
        const s = [styles.Grid, className, 'mp-grid'].join(' ')
        return <>
            <Container fluid className={s}
                {...this.props}
            />
        </>
    }
}

export default Grid;
