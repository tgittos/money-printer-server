import styles from "./Button.module.scss";
import Button, {IButtonProps} from "./Button";
import React from "react";
import {IconType} from "react-icons";

export interface IIconButtonProps extends IButtonProps {
    icon: IconType;
}

class IconButton extends React.Component<IIconButtonProps, {}> {
    render() {
        const { icon, ...p} = this.props;
        const s = [styles.IconButton, 'mp-icon-btn'];
        return <Button className={s.join(' ')} {...p}>
            { React.createElement(this.props.icon) }
        </Button>
    }
}

export default IconButton;
