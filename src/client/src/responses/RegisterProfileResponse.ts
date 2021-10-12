import {IProfile} from "../models/Profile";

interface IRegisterProfileResponse {
  success: boolean;
  message: string;
  data: IProfile;
}

export default IRegisterProfileResponse;
