import styles from "./Panel.module.scss";
import React from "react";
import PanelHeader from "./PanelHeader";
import PanelBody from "./PanelBody";
import PanelFooter from "./PanelFooter";

export interface IPanelProps extends React.ComponentPropsWithoutRef<any>{
    children?: React.ReactNode;
    className?: string;
}

export interface IPanelState {
}

class Panel extends React.Component<IPanelProps, IPanelState> {
    static Header = PanelHeader;
    static Body = PanelBody;
    static Footer = PanelFooter;

    render() {
        const s = [styles.Panel, 'mp-panel']
            .concat(Array.of(this.props.className))
            .join(' ');
        return <div className={s}>
            { this.props.children }
        </div>
    }
}

export default Panel;