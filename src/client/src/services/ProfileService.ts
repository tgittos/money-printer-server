import HttpService from "./HttpService";
import AuthService from "./AuthService";
import {IProfile} from "../models/Profile";

class ProfileService {

    private http: HttpService;
    private authService: AuthService;

    constructor() {
        this.http = new HttpService();
        this.authService = new AuthService();
    }

}

export default ProfileService;