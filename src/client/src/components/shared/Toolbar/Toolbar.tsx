import styles from "./Toolbar.module.scss";
import React from "react";
import IconButton from "../Button/IconButton";
import {Col, Row } from "react-bootstrap";

export interface IToolbarProps {
    orientation: "horizontal" | "vertical";
    children: IconButton[];
}

interface IToolbarState {

}

class Toolbar extends React.Component<IToolbarProps, IToolbarState> {
    private renderRow() {
        const s = [styles.Toolbar, 'mp-toolbar', 'mp-toolbar-horizontal'];
        return <Row className={s} {...this.props}>
            <Col className={styles.ToolbarCol}>
                { this.props.children.map(child => child) }
            </Col>
        </Row>
    }

    private renderCol() {
        return <Col className={styles.ToolbarVertical} {...this.props}>
            { this.props.children.map(child => child) }
        </Col>
    }

    render() {
        return this.props.orientation === "vertical"
            ? this.renderCol()
            : this.renderRow();
    }
}

export default Toolbar;
