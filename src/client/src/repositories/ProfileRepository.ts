import axios from 'axios';
import Cookies from 'universal-cookie';
import jwt from 'jwt-decode';

import AppStore from './../AppStore';
import { setCurrentProfile } from "../slices/ProfileSlice";

import BaseRepository from './BaseRepository'
import type IRegisterProfileRequest from '../requests/RegisterProfileRequest';
import type IRegisterProfileResponse from "../responses/RegisterProfileResponse";
import type IAuthProfileRequest from "../requests/AuthProfileRequest";
import type IAuthProfileResponse from "../responses/AuthProfileResponse";
import Env from '../env';
import IGetUnauthenticatedProfileResponse from "../responses/GetUnauthenticatedProfileResponse";
import Profile, {IServerProfile} from "../models/Profile";

class ProfileRepository extends BaseRepository {

  private JWT_TOKEN_KEY: string = "mp:jwt"

  _cookies: Cookies;

  constructor() {
    super();

    this.apiEndpoint = "auth/";
    this._cookies = new Cookies();
  }

  public async init(): Promise<void> {
    if (Env.DEBUG) {
      console.log("ProfileRepository::init - checking cookies for stored token");
    }

    const tokenProfile: Profile | null = this.hydrateJWTToken();
    if (tokenProfile) {
      if (Env.DEBUG) {
        console.log("ProfileRepository::init - found profile in token, setting profile to", tokenProfile);
      }
      AppStore.dispatch(setCurrentProfile(tokenProfile));
      return;
    }

    if (Env.DEBUG) {
      console.log("ProfileRepository::init - initializing unauthenticated user from server");
    }
    const response = await this.getUnauthenticatedProfile();
    if (response.success) {
      if (Env.DEBUG) {
        console.log("ProfileRepository::init - server return success message, setting profile to", response.data);
      }
      const data: IServerProfile = response.data;
      AppStore.dispatch(setCurrentProfile(new Profile(data)));
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
      const data: IServerProfile = response.data;
      AppStore.dispatch(setCurrentProfile(new Profile(data)));
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
      const data = response.data.profile as IServerProfile;
      this.storeToken(response.data.token);
      AppStore.dispatch(setCurrentProfile(new Profile(data)));
    }

    return response;
  }

  public logout() {
    this.clearToken();
    this.getUnauthenticatedProfile();
  }

  public reset_password(email: string) {
    throw new Error("not implemented");
  }

  private storeToken(token: string) {
    this._cookies.set(this.JWT_TOKEN_KEY, token);
  }

  private clearToken() {
    this._cookies.set(this.JWT_TOKEN_KEY, null);
  }

  private hydrateJWTToken(): Profile | null {
    const fetchedToken = this._cookies.get(this.JWT_TOKEN_KEY);
    if (fetchedToken) {
      const jwtProfile = jwt(fetchedToken);
      if (Env.DEBUG) {
        console.log('ProfileRepository::hydrateJWTToken - found profile:', jwtProfile);
      }
      if (jwtProfile?.profile) {
        return new Profile(jwtProfile.profile);
      }
    }
    return null;
  }
}

export default ProfileRepository;
