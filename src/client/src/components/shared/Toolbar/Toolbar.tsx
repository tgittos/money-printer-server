import styles from "./Toolbar.module.scss";
import React from "react";
import IconButton from "../Button/IconButton";
import {Col, Row } from "react-bootstrap";

export interface IToolbarProps {
    orientation: "horizontal" | "vertical";
    position: "top" | "bottom" | "left" | "right"
    children: IconButton[];
}

interface IToolbarState {

}

class Toolbar extends React.Component<IToolbarProps, IToolbarState> {
    private renderRow() {
        const s = [styles.Toolbar, 'mp-toolbar', 'mp-toolbar-horizontal',
            this.props.position ? this.props.position : 'top'];
        return <Row className={s.join(' ')} {...this.props}>
            <Col>
                { this.props.children.map(child => child) }
            </Col>
        </Row>
    }

    private renderCol() {
        const s = [styles.ToolbarVertical, 'mp-toolbar', 'mp-toolbar-vertical',
            this.props.position ? this.props.position : 'left'];
        return <Col xs={1} className={s.join(' ')} {...this.props}>
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
