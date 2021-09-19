import AppStore from './../stores/AppStore';
import {profileToIProfile, setCurrentProfile, setUnauthenticatedProfile} from "../slices/ProfileSlice";
import BaseRepository from './BaseRepository'
import type IRegisterProfileRequest from '../requests/RegisterProfileRequest';
import type IRegisterProfileResponse from "../responses/RegisterProfileResponse";
import type IAuthProfileRequest from "../requests/AuthProfileRequest";
import type IAuthProfileResponse from "../responses/AuthProfileResponse";
import Env from '../env';
import IGetUnauthenticatedProfileResponse from "../responses/GetUnauthenticatedProfileResponse";
import Profile from "../models/Profile";
import AuthService from "../services/AuthService";
import {setAppInitialized} from "../slices/AppSlice";
import AccountRepository from "./AccountRepository";

class ProfileRepository extends BaseRepository {

  private authService: AuthService;

  constructor() {
    super();

    this.apiEndpoint = "auth/";

    this.authService = new AuthService();
  }

  public async init(): Promise<void> {

    let profileToSet: Profile;

    if (Env.DEBUG) {
      console.log("ProfileRepository::init - checking cookies for stored token");
    }
    if (this.authService.currentProfile) {
      if (Env.DEBUG) {
        console.log("ProfileRepository::init - found profile in token, setting profile to", this.authService.currentProfile);
      }
      profileToSet = this.authService.currentProfile;
    }

    if (Env.DEBUG) {
      console.log("ProfileRepository::init - initializing unauthenticated user from server");
    }
    const response = await this.getUnauthenticatedProfile();
    if (response !== null) {
      const { token, profile } = response.data;

      const unauthenticatedProfile = new Profile(profile);
      if (!profileToSet) {
        this.authService.setProfile(token);
        profileToSet = unauthenticatedProfile;
      }
      AppStore.dispatch(setAppInitialized());
      AppStore.dispatch(setUnauthenticatedProfile(profileToIProfile(unauthenticatedProfile)));
    }

    if (Env.DEBUG) {
      console.log("ProfileRepository::init - setting profile to", profileToSet);
    }
    AppStore.dispatch(setCurrentProfile(profileToIProfile(profileToSet)));
  }

  public async getUnauthenticatedProfile(): Promise<IGetUnauthenticatedProfileResponse> {
    const response = await this.unauthenticatedRequest<null, IGetUnauthenticatedProfileResponse>({
          url: this.endpoint + "unauthenticated"
        }).then(response => (response.data as unknown) as IGetUnauthenticatedProfileResponse);
    if (response.success) {
      const unauthedProfile = new Profile(response.data.profile);
      AppStore.dispatch(setCurrentProfile(unauthedProfile));
    }
    return response;
  }

  public async invite(request: IRegisterProfileRequest): Promise<IRegisterProfileResponse> {
    const response = this.unauthenticatedRequest<IRegisterProfileRequest,IRegisterProfileResponse>({
          method: "POST",
          url: this.endpoint + "register",
          data: {
            username: request.email,
            firstName: request.firstName,
            lastName: request.lastName
          }});
    return response;
  }

  public async auth(request: IAuthProfileRequest): Promise<IAuthProfileResponse> {
    if (Env.DEBUG) {
      console.log('ProfileRepository::auth - performing auth with request:', request);
    }

    const response = await this.unauthenticatedRequest<IAuthProfileRequest, IAuthProfileResponse>({
      method: "POST",
      url: this.endpoint + "login",
      data: {
        username: request.username,
        password: request.password
      }
    }).then(response => (response.data as unknown) as IAuthProfileResponse);

    if (Env.DEBUG) {
      console.log('ProfileRepository::auth - response from server:', response);
    }

    if (response.success) {
      const serverProfile = response.data.profile;
      const authedProfile = new Profile(serverProfile);
      this.authService.setProfile(response.data.token);
      AppStore.dispatch(setCurrentProfile(authedProfile));
    }

    return response;
  }

  public logout() {
    this.authService.clearProfile();
    this.getUnauthenticatedProfile();
  }

  public reset_password(email: string) {
    throw new Error("not implemented");
  }
}

export default ProfileRepository;
