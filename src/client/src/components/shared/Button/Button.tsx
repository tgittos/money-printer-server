import styles from "./Button.module.scss";
import React  from "react";
import { Button as ReactButton } from "react-bootstrap";

export interface IButtonProps extends React.ComponentPropsWithoutRef<ReactButton> {
    // wraps the React button's variant so we can always set it to outline
    variant?: string;
    className?: string | object;
}

export interface IButtonState {

}

class Button extends React.Component<IButtonProps, IButtonState> {

    private get variant(): string {
        let variant = "outline";
        if (this.props.variant) {
            variant += "-" + this.props.variant
        }
        return variant;
    }

    render() {
        return <ReactButton
            className={this.props.className ?? styles.Button}
            variant={this.variant}
            {...this.props}
        />
    }
}

export default Button;
