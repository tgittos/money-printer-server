import React from "react";
import styles from "./Panel.module.scss";

export interface IPanelBodyProps {
    children: React.ReactNode;
}

export interface IPanelBodyState {

}

class PanelBody extends React.Component<IPanelBodyProps, IPanelBodyState> {
    render() {
        return <div className={styles.PanelBody}>
            { this.props.children }
        </div>
    }
}

export default PanelBody;
