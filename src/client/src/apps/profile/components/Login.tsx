import styles from "./../Profile.module.scss";
import Button from "../../../components/shared/Button/Button";
import Panel from "../../../components/shared/Panel/Panel";
import {profileReducer, ProfileAction, SET_PROFILE, initialProfileState, ProfileContext} from "../Profile.state";
import {useContext, useEffect, useReducer, useState} from "react";
import {useRecoilValue, useSetRecoilState} from "recoil";
import {IProfile} from "../../../models/Profile";
import ProfileService from "../../../services/ProfileService";

const Login = () => {
    const classes = [
        'mp-login',
        styles.Login
    ];

    const { dispatch } = useContext(ProfileContext);
    const [email, setEmail] = useState("");
    const [password, setPassword] = useState("");
    const auth = async () => {
        const profileService = new ProfileService();
        const profile = await profileService.authenticateProfile(email, password);
        dispatch({
            type: SET_PROFILE,
            payload: profile
        } as ProfileAction);
    };

    return <Panel className={classes.join(' ')}>
       <p>
           <input type="text"  placeholder="Email"
                  value={email}
                  onChange={(el) => setEmail(el.target.value) }
           />
       </p>
        <p>
            <input type="password"  placeholder="Password"
                   value={password}
                   onChange={(el) => setPassword(el.target.value)}
            />
        </p>
        <p>
            <Button primary={true} onClick={auth}>
                Login
            </Button>
        </p>
    </Panel>
}

export default Login;
