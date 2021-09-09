import Profile from "../models/Profile";

export interface IAuthedProfile {
    profile: Profile
    token: string
}

interface IAuthProfileResponse {
    success: boolean;
    message: string;
    data: IAuthedProfile
}

export default IAuthProfileResponse;
