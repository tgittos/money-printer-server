import React from 'react';
import styles from './BigLoader.module.scss';

type BigLoaderProps = {};
type BigLoaderState = {};

class Login extends React.Component<BigLoaderState, BigLoaderProps> {

    render() {
        return (
            <div className={styles.BigLoader}>
                <img src="/loaders/nyan.gif"
                     width="450"
                     height="450"
                     alt="Loading spinner"
                     />
            </div>
        );
    }
}

export default Login;
