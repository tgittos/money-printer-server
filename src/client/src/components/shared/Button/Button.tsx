import styles from "./Button.module.scss";
import React  from "react";
import { Button as ReactButton } from "react-bootstrap";

export interface IButtonProps extends React.ComponentPropsWithoutRef<ReactButton> {
    // wraps the React button's variant so we can always set it to outline
    primary?: boolean;
    secondary?: boolean;
    disabled?: boolean;
    outline?: boolean;
    link?: boolean;
    small?: boolean;
    medium?: boolean;
    large?: boolean;
    xl?: boolean;
    full?: boolean;
    className?: string | object;
}

export interface IButtonState {

}

class Button extends React.Component<IButtonProps, IButtonState> {

    private get highestSize(): string {
        const { small, medium, large, xl, full} = this.props;
        if (full) return 'full';
        if (xl) return 'xl';
        if (large) return 'lg';
        if (medium) return null;
        if (small) return 'sm';
        return null;
    }

    private get variant(): string {
        let prefix = '';
        const { primary, secondary, disabled, outline, link } = this.props;
        if (outline) prefix = 'outline-';
        if (disabled) return prefix + "disabled";
        if (primary) return prefix + "primary";
        if (secondary) return prefix + "secondary";
        if (link) return "link";
        if (outline) return "outline";
        return null;
    }

    render() {
        const size = this.highestSize;
        const variant = this.variant;

        let s = [styles.Button];
        if (this.props.className) s = s.concat(Array.of(this.props.className));

        return <ReactButton
            className={s}
            variant={variant}
            size={size}
            {...this.props}
        />
    }
}

export default Button;
