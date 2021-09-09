import React from 'react';
import styles from './ErrorMessage.module.scss';

type ErrorMessageProps = {
    message: string;
    inline: boolean;
}

class ErrorMessage extends React.Component<ErrorMessageProps, {}> {

    renderInline() {
        return <span className={styles.ErrorMessage}>
            {this.props.message}
        </span>
    }

    renderBlock() {
        return <div className={styles.ErrorMessage}>
            {this.props.message}
        </div>;
    }

    render() {
        if (this.props.inline) {
            return this.renderInline();
        }
        return this.renderBlock();
    }
};

export default ErrorMessage;
