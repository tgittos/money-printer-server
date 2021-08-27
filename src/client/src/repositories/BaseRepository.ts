import Env from '../env';

class BaseRepository {

  apiEndpoint: string = "";


  public get endpoint() {
    return "http://" + Env.API_HOST + "/" + Env.API_VERSION + "/api/" + this.apiEndpoint;
  }
}

export default BaseRepository;
