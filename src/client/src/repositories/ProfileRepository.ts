import axios from 'axios';

import BaseRepository from './BaseRepository'
import type IRegisterProfileRequest from '../requests/RegisterProfileRequest';
import type IRegisterProfileResponse from "../responses/RegisterProfileResponse";
import type IAuthProfileRequest from "../requests/AuthProfileRequest";
import type IAuthProfileResponse from "../responses/AuthProfileResponse";
import Profile from "../models/Profile";
import Env from '../env';

class ProfileRepository extends BaseRepository {

  private _currentProfile: Profile = new Profile();

  constructor() {
    super();

    this.apiEndpoint = "auth/";
  }

  public getCurrentProfile(): Profile {
    return this._currentProfile;
  }

  public async register(request: IRegisterProfileRequest): Promise<IRegisterProfileResponse> {
    const response: any =
        await axios.request<IRegisterProfileRequest>({
        url: this.endpoint + "register",
        data: {
          username: request.email,
          firstName: request.firstName,
          lastName: request.lastName
        }
      }).then(response => response.data);

    this._setCurrentProfile(response);

    return response;
  }

  public auth(request: IAuthProfileRequest): IAuthProfileResponse {
    const response = axios.request<IAuthProfileRequest>({
      url: this.endpoint + "login",
      data: {
        username: request.username,
        password: request.password
      }
    }).then(response => response.data);

    return response;
  }

  public logout(email: string) {
    throw new Error("not implemented");
  }

  public reset_password(email: string) {
    throw new Error("not implemented");
  }

  private _setCurrentProfile(response: IRegisterProfileResponse) {
    if (!response.success) {
      if (Env.DEBUG) {
        console.log('ProfileRepository::_setCurrentProfile error response from API:', response.message);
      }
      return;
    }

    this._currentProfile = response.data;
  }
}

export default ProfileRepository;
