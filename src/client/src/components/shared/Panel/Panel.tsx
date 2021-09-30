import styles from "./Panel.module.scss";
import React from "react";
import PanelHeader from "./PanelHeader";
import PanelBody from "./PanelBody";
import PanelFooter from "./PanelFooter";

export interface IPanelProps {
    children?: React.ReactNode;
}

export interface IPanelState {
}

class Panel extends React.Component<IPanelProps, IPanelState> {
    render() {
        return <div className={styles.Panel}>
            { this.props.children }
        </div>
    }
}

Panel.Header = PanelHeader;
Panel.Body = PanelBody;
Panel.Footer = PanelFooter;

export default Panel;