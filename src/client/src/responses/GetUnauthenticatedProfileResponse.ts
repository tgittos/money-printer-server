import {IAuthedProfile} from "../models/Profile";

interface IGetUnauthenticatedProfileResponse {
    success: boolean;
    message: string;
    data: IAuthedProfile;
}

export default IGetUnauthenticatedProfileResponse;
