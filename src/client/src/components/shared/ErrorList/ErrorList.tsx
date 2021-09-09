import React from 'react';
import styles from './ErrorList.module.scss';
import ErrorMessage from "../ErrorMessage/ErrorMessage";

type ErrorListProps = {
    messages: string[];
    inline: boolean;
}

class ErrorList extends React.Component<ErrorListProps, {}> {

    render() {
        return <div className={styles.ErrorList}>
            {this.props.messages.map(message => {
                return (
                    <ErrorMessage message={message} inline={this.props.inline}>
                    </ErrorMessage>
                )
            })}
        </div>
    }
};

export default ErrorList;
