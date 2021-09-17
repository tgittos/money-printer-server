import Env from '../env';
import AuthService from "../services/AuthService";
import HttpService from "../services/HttpService";

class BaseRepository {

  protected apiEndpoint: string = "";
  protected http: HttpService;

  constructor() {
    this.http = new HttpService();
  }

  public get endpoint() {
    return this.http.baseApiEndpoint + "/" + this.apiEndpoint;
  }

  public async authenticatedRequest<ReqT, ResT>(opts: any): Promise<ResT> {
    return this.http.authenticatedRequest(opts);
  }

  public async unauthenticatedRequest<ReqT, ResT>(opts: any): Promise<ResT> {
    return this.http.unauthenticatedRequest(opts);
  }
}

export default BaseRepository;
