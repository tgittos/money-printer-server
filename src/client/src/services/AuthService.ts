import Cookies from "universal-cookie";
import Profile, {IProfile} from "../models/Profile";
import HttpService from "./HttpService";
import type {AppDispatch} from "../store/AppStore";
import {useAppDispatch, useAppSelector} from "../store/AppHooks";
import {ClearCurrentProfile} from "../store/actions/ProfileActions";
import {AuthenticateUser, InitializeUnauthenticated} from "../store/thunks/ProfileThunks";
import jwt from "jwt-decode";
import {IProfileState} from "../store/reducers/ProfileReducers";

export type NullableProfile = Profile | null;

class AuthService {

    private JWT_TOKEN_KEY: string = "mp:jwt"
    readonly cookies: Cookies;
    private tokenProfile: NullableProfile;
    readonly http: HttpService;
    readonly selector: () => IProfileState;
    readonly dispatch: AppDispatch;

    public get currentProfile(): NullableProfile {
        return this.tokenProfile
    }
    public get token(): string {
        return this.getToken();
    }

    private get endpoint(): string {
        return this.http.baseApiEndpoint + "/auth"
    }

    constructor() {
        this.http = new HttpService();
        this.cookies = new Cookies();
        this.selector = useAppSelector((state) => {
            const { profiles } = state;
            return () => profiles as IProfileState;
        });
        this.dispatch = useAppDispatch();
    }

    public async auth(username: string, password: string): Promise<Profile> {
        if (this.selector().authenticated) {
            // already authed, we can just return a synthetic response
        }
        this.dispatch(AuthenticateUser({ username, password }));
    }

    public loadProfileFromToken(): Profile | null {
        let loadedProfile: Profile = null;
        const fetchedToken = this.getToken();
        if (fetchedToken) {
            const jwtProfile: any = jwt(fetchedToken);
            if (jwtProfile?.profile) {
                loadedProfile = new Profile(jwtProfile.profile as IProfile);
            }
        }
        this.tokenProfile = loadedProfile;
        return loadedProfile;
    }

    public logout() {
        this.dispatch(ClearCurrentProfile());
        this.dispatch(InitializeUnauthenticated());
    }

    public resetPassword(email: string) {
        throw new Error("not implemented");
    }

    public setToken(token: string) {
        this.cookies.set(this.JWT_TOKEN_KEY, token);
    }

    private getToken() {
        return this.cookies.get(this.JWT_TOKEN_KEY);
    }

    public clearToken() {
        this.cookies.remove(this.JWT_TOKEN_KEY);
    }
}

export default AuthService;
