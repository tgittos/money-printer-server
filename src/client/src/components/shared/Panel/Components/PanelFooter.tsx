import React from "react";
import styles from "../Panel.module.scss";
import Button from "../../Button/Button";
import {IPanelHeaderProps} from "./PanelHeader";

export interface IPanelFooterProps {
    children: Button | Button[];
}

export interface IPanelFooterState {

}

class PanelFooter extends React.Component<IPanelFooterProps, IPanelFooterState> {
    render() {
        const { className } = (this.props as IPanelHeaderProps);
        let s = [styles.PanelFooter, 'mp-panel-footer'];
        if (className) s = s.concat(Array.of(className))
        return <div className={s.join(' ')}>
            { this.props.children }
        </div>
    }
}

export default PanelFooter;
