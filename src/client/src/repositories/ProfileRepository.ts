import axios from 'axios';

import BaseRepository from './BaseRepository'
import type IRegisterProfileRequest from '../requests/RegisterProfileRequest';
import type IRegisterProfileResponse from "../responses/RegisterProfileResponse";
import type IAuthProfileRequest from "../requests/AuthProfileRequest";
import type IAuthProfileResponse from "../responses/AuthProfileResponse";
import Profile from "../models/Profile";
import Env from '../env';
import IGetUnauthenticatedProfileResponse from "../responses/GetUnauthenticatedProfileResponse";
import {BehaviorSubject, Observable } from "rxjs";

class ProfileRepository extends BaseRepository {

  public get currentProfile$(): Observable<Profile | null> {
    return this._profileSubject.asObservable();
  }
  public get currentProfile(): Profile | null {
    return this._profileSubject.getValue();
  }
  private _profileSubject: BehaviorSubject<Profile | null> = new BehaviorSubject<Profile | null>(null);

  constructor() {
    super();

    this.apiEndpoint = "auth/";

    this.init();
  }

  private async init(): Promise<void> {
    if (Env.DEBUG) {
      console.log("ProfileRepository::init - initializing unauthenticated user from server");
    }
    const response = await this.getUnauthenticatedProfile();
    if (response.success) {
      if (Env.DEBUG) {
        console.log("ProfileRepository::init - server return success message, setting profile to", response.data);
      }
      this._profileSubject.next(response.data);
      return;
    }
    if (Env.DEBUG) {
      console.log("ProfileRepository::init - server return non-success message, setting profile to null");
    }
    this._profileSubject.next(null);
  }

  public async getUnauthenticatedProfile(): Promise<IGetUnauthenticatedProfileResponse> {
    const response: IGetUnauthenticatedProfileResponse =
        await axios.request({
          url: this.endpoint + "unauthenticated"
        }).then(response => response.data) as IGetUnauthenticatedProfileResponse;
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

  public auth(request: IAuthProfileRequest): IAuthProfileResponse {
    const response = axios.request<IAuthProfileRequest>({
      method: "POST",
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
}

export default ProfileRepository;
