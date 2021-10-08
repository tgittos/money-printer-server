import {IAppState} from "../slices/AppSlice";
import AuthService from "../../services/AuthService";
import {useAppDispatch} from "../AppHooks";
import {InitializeUnauthenticated} from "../thunks/ProfileThunks";
import {Initialize} from "../actions/AppActions";
import {SetCurrentProfile} from "../actions/ProfileActions";

const authService = new AuthService();
const dispatch = useAppDispatch();

export const appReducers = {
    [Initialize.type]: (state: IAppState, action) => {
        // all the server side bootstrapping gets triggered from here

        // bootstrap the app with either a previously authed user account
        // or initialize the application with the unauthenticated user state
        if (authService.currentProfile) {
            dispatch(SetCurrentProfile(authService.currentProfile, true));
        } else {
            dispatch(InitializeUnauthenticated());
        }
    },
};
