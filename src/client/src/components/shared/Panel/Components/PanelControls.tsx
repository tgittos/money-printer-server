import styles from "./../Panel.module.scss";
import React from "react";
import PanelControlClose from "./Controls/PanelControlClose";
import PanelControlMaximize from "./Controls/PanelControlMaximize";
import PanelControlMinimize from "./Controls/PanelControlMinimize";

export interface IPanelControlsProps extends React.ComponentPropsWithoutRef<any> {
    children?: React.ReactNode;
    className?: string;
}

class PanelControls extends React.Component<IPanelControlsProps, any> {
    static Close = PanelControlClose;
    static Maximize = PanelControlMaximize;
    static Minimize = PanelControlMinimize;

    render() {
        let s = [styles.PanelControls, 'mp-panel-header-controls']
        if (this.props.className) s = s.concat(Array.of(this.props.className));
        return <div className={s.join(' ')}>
            { this.props.children }
        </div>;
    }
}

export default PanelControls;