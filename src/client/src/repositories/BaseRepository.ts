import Env from '../env';
import axios from "axios";
import AuthService from "../services/AuthService";

class BaseRepository {

  protected  apiEndpoint: string = "";
  protected authService: AuthService;

  constructor() {
    this.authService = new AuthService();
    this.wireAuthInterceptors();
  }

  public get endpoint() {
    return "http://" + Env.API_HOST + "/" + Env.API_VERSION + "/api/" + this.apiEndpoint;
  }

  public async unauthenticatedRequest<ReqT, ResT>(opts: any): Promise<ResT> {
    return await axios.request<ReqT>(
        opts
      ).then(response => (response as unknown) as ResT);
  }

  public async authenticatedRequest<ReqT, ResT>(opts: any): Promise<ResT> {
    const token = this.authService.token;
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
            console.log('BaseRepository::wireAuthInterceptors - axios response interceptor: received 401 from server, clearing auth information');
          }
          // this.authService.clearProfile();
          // AppStore.dispatch(clearCurrentProfile());
        }
      }
      return Promise.reject(error);
    })
  }

}

export default BaseRepository;
