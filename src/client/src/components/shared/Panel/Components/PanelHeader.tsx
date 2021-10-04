import React, {ReactNode} from "react";
import styles from "../Panel.module.scss";
import PanelControls from "./PanelControls";

export interface IPanelControl {
    icon: React.ReactNode;
    eventKey: string;
}

export interface IPanelHeaderProps extends React.ComponentPropsWithoutRef<any> {
    children: React.ReactNode;
    className?: string;
    controls?: IPanelControl[];
}

export interface IPanelHeaderState {

}

class PanelHeader extends React.Component<IPanelHeaderProps, IPanelHeaderState> {
    static Controls = PanelControls;
    render() {
        const { className } = (this.props as IPanelHeaderProps);
        let s = [styles.PanelTitle, 'mp-panel-header'];
        if (className) s = s.concat(Array.of(className))
        return <div className={s.join(' ')}>
            { this.props.children }
        </div>
    }
}

export default PanelHeader;
