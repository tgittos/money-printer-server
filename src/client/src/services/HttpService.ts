import axios from "axios";
import Env from "../env";
import AuthService from "./AuthService";
import {ClearCurrentProfile} from "../store/actions/ProfileActions";

class HttpService {

    private authService: AuthService;

    public get baseApiEndpoint() {
        return "http://" + Env.API_HOST + "/" + Env.API_VERSION + "/api";
    }

    constructor() {
        this.authService = new AuthService();
        this.wireAuthInterceptors();
    }

    public async unauthenticatedRequest<ReqT, ResT>(opts: any): Promise<ResT> {
        return await axios.request<ReqT>(
            opts
        ).then(response => (response as unknown) as ResT);
    }

    public async authenticatedRequest<ReqT, ResT>(opts: any): Promise<ResT> {
        const token = this.authService.token;
        if (token === undefined) {
            // authed request requested, but no token present (logged in as anonymous user, likely)
            // fallback to an unauthed request
            if (Env.DEBUG) {
                console.log('loaded undefined token from auth service, falling back to unauthed request');
            }
            return this.unauthenticatedRequest<ReqT, ResT>(opts)
                .then(response => (response as unknown) as ResT);
        }
        return await axios.request<ReqT>({
            ...opts,
            headers: {
                Authorization: `Bearer ${token}`
            }
        }).then(response => (response as unknown) as ResT);
    }

    private wireAuthInterceptors() {
        axios.interceptors.response.use(response => {
            return response;
        }, error => {
            if (error.response !== undefined) {
                const {status} = error.response;
                if (status === 401) {
                    if (Env.DEBUG) {
                        console.log('HttpService::wireAuthInterceptors - axios response interceptor: received 401 from server, clearing auth information');
                    }
                    this.authService.logout();
                    // useAppDispatch()(ClearCurrentProfile());
                }
            }
            return Promise.reject(error);
        })
    }
}

export default HttpService;