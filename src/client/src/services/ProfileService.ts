import HttpService from "./HttpService";
import AuthService from "./AuthService";
import Profile, {IProfile} from "../models/Profile";
import IGetUnauthenticatedProfileResponse from "../responses/GetUnauthenticatedProfileResponse";
import IAuthProfileRequest from "../requests/AuthProfileRequest";
import IAuthProfileResponse from "../responses/AuthProfileResponse";

class ProfileService {

    private http: HttpService;
    private authService: AuthService;

    constructor() {
        this.http = new HttpService();
        this.authService = new AuthService();
    }

    public async fetchAnonymousProfile(): Promise<IProfile> {
        const response = await this.http.unauthenticatedRequest<null, IGetUnauthenticatedProfileResponse>({
            url: this.http.baseApiEndpoint + "/auth/unauthenticated"
        }).then(response => (response.data as unknown) as IGetUnauthenticatedProfileResponse);
        if (response.success) {
            return response.data.profile;
        }
        throw new Error(response.message);
    }

    public async authenticateProfile(username: string, password: string): Promise<IProfile> {
        const response = await this.http.unauthenticatedRequest<IAuthProfileRequest, IAuthProfileResponse>({
            method: "POST",
            url: this.http.baseApiEndpoint + "/auth/login",
            data: { username, password }
        })
            .then(response => (response.data as unknown) as IAuthProfileResponse);
        if (response.success) {
            return response.data.profile;
        }
        throw new Error(response.message);
    }

}

export default ProfileService;