import React from "react";
import styles from "../Panel.module.scss";
import {IPanelHeaderProps} from "./PanelHeader";

export interface IPanelBodyProps extends React.ComponentPropsWithoutRef<any> {
    children: React.ReactNode;
    className?: string;
}

export interface IPanelBodyState {

}

class PanelBody extends React.Component<IPanelBodyProps, IPanelBodyState> {
    render() {
        const { className } = (this.props as IPanelHeaderProps);
        let s = [styles.PanelBody, 'mp-panel-body'];
        if (className) s = s.concat(Array.of(className))
        return <div className={s.join(' ')}>
            { this.props.children }
        </div>
    }
}

export default PanelBody;
