import axios from 'axios';

import AppStore from './../AppStore';
import { setCurrentProfile } from "../slices/ProfileSlice";

import BaseRepository from './BaseRepository'
import type IRegisterProfileRequest from '../requests/RegisterProfileRequest';
import type IRegisterProfileResponse from "../responses/RegisterProfileResponse";
import type IAuthProfileRequest from "../requests/AuthProfileRequest";
import type IAuthProfileResponse from "../responses/AuthProfileResponse";
import Env from '../env';
import IGetUnauthenticatedProfileResponse from "../responses/GetUnauthenticatedProfileResponse";

class ProfileRepository extends BaseRepository {

  constructor() {
    super();

    this.apiEndpoint = "auth/";
  }

  public async init(): Promise<void> {
    if (Env.DEBUG) {
      console.log("ProfileRepository::init - initializing unauthenticated user from server");
    }
    const response = await this.getUnauthenticatedProfile();
    if (response.success) {
      if (Env.DEBUG) {
        console.log("ProfileRepository::init - server return success message, setting profile to", response.data);
      }
      AppStore.dispatch(setCurrentProfile(response.data));
      return;
    }

    if (Env.DEBUG) {
      console.log("ProfileRepository::init - server return non-success message");
    }
  }

  public async getUnauthenticatedProfile(): Promise<IGetUnauthenticatedProfileResponse> {
    const response: IGetUnauthenticatedProfileResponse =
        await axios.request({
          url: this.endpoint + "unauthenticated"
        }).then(response => response.data) as IGetUnauthenticatedProfileResponse;
    if (response.success) {
      AppStore.dispatch(setCurrentProfile(response.data));
    }
    return response;
  }

  public async invite(request: IRegisterProfileRequest): Promise<IRegisterProfileResponse> {
    const response: any =
        await axios.request<IRegisterProfileRequest>({
          method: "POST",
          url: this.endpoint + "register",
          data: {
            username: request.email,
            firstName: request.firstName,
            lastName: request.lastName
          }
        }).then(response => response.data);
    return response;
  }

  public async auth(request: IAuthProfileRequest): Promise<IAuthProfileResponse> {
    if (Env.DEBUG) {
      console.log('ProfileRepository::auth - performing auth with request:', request);
    }

    const response:IAuthProfileResponse = await axios.request<IAuthProfileRequest>({
      method: "POST",
      url: this.endpoint + "login",
      data: {
        username: request.username,
        password: request.password
      }
    }).then(response => response.data) as IAuthProfileResponse;

    if (Env.DEBUG) {
      console.log('ProfileRepository::auth - response from server:', response);
    }

    if (response.success) {
      if (Env.DEBUG) {
        console.log('ProfileRepository::auth - setting next value on this._profileSubject:', response.data);
      }
      AppStore.dispatch(setCurrentProfile(response.data));
    }

    return response;
  }

  public logout(email: string) {
    throw new Error("not implemented");
  }

  public reset_password(email: string) {
    throw new Error("not implemented");
  }
}

export default ProfileRepository;
