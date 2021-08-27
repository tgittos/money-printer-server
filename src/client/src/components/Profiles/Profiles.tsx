import React from 'react';
import styles from './Profiles.module.scss';

type ProfilesProps = {
}

type ProfilesState = {
}

class Profiles extends React.Component<ProfilesProps, ProfilesState> {

    render() {
        return <div className={styles.Profiles}>
            Profiles Component
        </div>
    }
}

export default Profiles;
