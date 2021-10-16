import Cookies from "universal-cookie";
import Profile, {IProfile} from "../models/Profile";
import HttpService from "./HttpService";
import jwt from "jwt-decode";

export type NullableProfile = Profile | null;

class AuthService {

    private JWT_TOKEN_KEY: string = "mp:jwt"
    readonly cookies: Cookies;
    private tokenProfile: NullableProfile;

    public get currentProfile(): NullableProfile {
        return this.tokenProfile
    }
    public get token(): string {
        return this.getToken();
    }

    constructor() {
        this.cookies = new Cookies();

        this.loadProfileFromToken();
    }

    public async auth(username: string, password: string): Promise<void> {
        //if (this.selector().authenticated && this.currentProfile) {
            // already authed, we can just return the current profile
        //     return new Promise<Profile>(p => p(this.currentProfile))
        //}
        // not authed, or missing profile, lets fire an auth request
        // this.dispatch(AuthenticateUser({ username, password }));
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
        // this.dispatch(ClearCurrentProfile());
        // this.dispatch(InitializeUnauthenticated());
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
