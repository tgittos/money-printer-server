import Profile from "../models/Profile";

interface IAuthProfileResponse {
    success: boolean;
    message: string;
    data: Profile
}

export default IAuthProfileResponse;
