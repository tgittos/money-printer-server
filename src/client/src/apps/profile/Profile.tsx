import React, {useReducer} from "react";
import ProfileModel, {IProfile} from './../../models/Profile';
import {Route, Switch} from "react-router-dom";
import Login from "./components/Login";
import {ProfileContext, initialProfileState, profileReducer} from './Profile.state';


export interface IProfileProps {
    profile: ProfileModel;
}


const Profile = (props: IProfileProps) => {
    const [state, dispatch] = useReducer(profileReducer, initialProfileState);

    return <ProfileContext.Provider value={{state, dispatch}}>
        <div>
            <Switch>
                <Route path="/profile" exact>
                   Profile dashboard
                </Route>
                <Route path="/profile/login">
                    <Login />
                </Route>
            </Switch>
        </div>
    </ProfileContext.Provider>
}

export default Profile;
