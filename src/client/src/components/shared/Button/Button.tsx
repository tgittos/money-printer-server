import React, {ReactNode} from "react";
import { Button as ReactButton } from "react-bootstrap";

export interface IButtonProps {
    children: ReactNode;
    variant: string;
    size: string;
    active: boolean;
    disabled: boolean;
}

export interface IButtonState {

}

class Button extends React.Component<IButtonProps, IButtonState> {
    render() {
        return <ReactButton
            variant={"outline-" + this.props.variant}
            size={this.props.size}
            active={this.props.active}
            disabled={this.props.disabled}
        >{ this.props.children }</ReactButton>
    }
}

export default Button;
