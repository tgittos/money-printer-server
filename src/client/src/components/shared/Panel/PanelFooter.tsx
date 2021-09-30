import React from "react";
import styles from "./Panel.module.scss";
import Button from "../Button/Button";

export interface IPanelFooterProps {
    children: Button | Button[];
}

export interface IPanelFooterState {

}

class PanelFooter extends React.Component<IPanelFooterProps, IPanelFooterState> {
    render() {
        return <div className={styles.PanelFooter}>
            { this.props.children }
        </div>
    }
}

export default PanelFooter;
