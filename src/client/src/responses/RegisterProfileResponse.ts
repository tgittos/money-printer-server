import {IServerProfile} from "../models/Profile";

interface IRegisterProfileResponse {
  success: boolean;
  message: string;
  data: IServerProfile;
}

export default IRegisterProfileResponse;
