import Profile, {IServerProfile} from "../models/Profile";

interface IGetUnauthenticatedProfileResponse {
    success: boolean;
    message: string;
    data: IServerProfile;
}

export default IGetUnauthenticatedProfileResponse;
