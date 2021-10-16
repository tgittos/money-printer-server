import styles from "./Button.module.scss";
import React  from "react";
import { Button as ReactButton } from "react-bootstrap";

export interface IButtonProps extends React.ComponentPropsWithoutRef<any> {
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
    className?: string;
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
        return "primary";
    }

    render() {
        const { className } = this.props;

        const size = this.highestSize;
        const variant = this.variant;

        let s = [styles.Button, size];
        if (this.props.className) s = s.concat(Array.of(className));

        // suppressing a linting complaint about size only accepting 'sm' or 'lg'
        // we know that, we don't care, we define other variants in our theme

        // @ts-ignore
        return <ReactButton
            className={s.join(' ')}
            variant={variant}
            {...this.props}
        />
    }
}

export default Button;
