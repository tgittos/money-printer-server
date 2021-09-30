import React from "react";
import styles from "./Panel.module.scss";

export interface IPanelControl {
    icon: React.ReactNode,
    eventKey: string
}

export interface IPanelHeaderProps {
    children: React.ReactNode;
    controls?: IPanelControl[];
}

export interface IPanelHeaderState {

}

class PanelHeader extends React.Component<IPanelHeaderProps, IPanelHeaderState> {
    render() {
        return <div className={styles.PanelTitle}>
            { this.props.children }
        </div>
    }
}

export default PanelHeader;
