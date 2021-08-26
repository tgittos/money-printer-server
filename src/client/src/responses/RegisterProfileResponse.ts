import Profile from "../models/Profile";

interface IRegisterProfileResponse {
  success: boolean;
  message: string;
  data: Profile;
}

export default IRegisterProfileResponse;
