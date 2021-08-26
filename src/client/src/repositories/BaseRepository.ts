import Env from '../env';

class BaseRepository {

  apiEndpoint: string = "";


  public get endpoint() {
    return Env.API_HOST + "/api/" + Env.API_VERSION + "/" + this.apiEndpoint;
  }
}

export default BaseRepository;
