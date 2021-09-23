import Cookies from "universal-cookie";
import Profile, {IProfile, IServerProfile} from "../models/Profile";
import jwt from "jwt-decode";
import Env from "../env";

export type NullableProfile = Profile | null;

class AuthService {

    private JWT_TOKEN_KEY: string = "mp:jwt"
    private cookies: Cookies;
    private tokenProfile: NullableProfile;

    public get currentProfile(): NullableProfile {
        return this.tokenProfile
    }
    public get token(): string {
        return this.getToken();
    }

    constructor() {
        this.cookies = new Cookies();
    }

    public setProfile(token: string) {
        this.storeToken(token);
        this.tokenProfile = this.loadProfileFromToken();
    }

    public clearProfile() {
        this.clearToken()
        this.tokenProfile = null;
    }

    public loadProfileFromToken(): Profile | null {
        let loadedProfile: Profile = null;
        const fetchedToken = this.getToken();
        if (fetchedToken) {
            const jwtProfile: any = jwt(fetchedToken);
            if (jwtProfile?.profile) {
                loadedProfile = new Profile(jwtProfile.profile as IServerProfile);
            }
        }
        this.tokenProfile = loadedProfile;
        return loadedProfile;
    }

    protected storeToken(token: string) {
        this.cookies.set(this.JWT_TOKEN_KEY, token);
    }

    protected getToken() {
        return this.cookies.get(this.JWT_TOKEN_KEY);
    }

    private clearToken() {
        this.cookies.remove(this.JWT_TOKEN_KEY);
    }
}

export default AuthService;
