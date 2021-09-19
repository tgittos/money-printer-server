import {IAuthedProfile} from "../models/Profile";

interface IAuthProfileResponse {
    success: boolean;
    message: string;
    data: IAuthedProfile
}

export default IAuthProfileResponse;
