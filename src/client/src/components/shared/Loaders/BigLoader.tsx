import React from 'react';
import styles from './BigLoader.module.scss';

type BigLoaderProps = {};
type BigLoaderState = {};

class Login extends React.Component<BigLoaderState, BigLoaderProps> {

    constructor(props: BigLoaderProps) {
        super(props);
    }

    render() {
        return (
            <div className={styles.BigLoader}>
                <img src="/loaders/nyan.gif"
                     width="450"
                     height="450"
                     />
            </div>
        );
    }
}

export default Login;
