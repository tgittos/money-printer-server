import Profile from "../models/Profile";

interface IGetUnauthenticatedProfileResponse {
    success: boolean;
    message: string;
    data: Profile;
}

export default IGetUnauthenticatedProfileResponse;
