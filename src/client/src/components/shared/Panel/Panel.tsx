import styles from "./Panel.module.scss";
import React from "react";

export interface IPanelProps {
    title?: string;
    children?: React.ReactNode;
}

export interface IPanelState {
}

class Panel extends React.Component<IPanelProps, IPanelState> {
    render() {
        return <div className={styles.Panel}>
            { this.props.title && <div className={styles.PanelTitle}>
                { this.props.title }
            </div> }
            <div className={styles.PanelBody}>
                { this.props.children }
            </div>
        </div>
    }
}

export default Panel;