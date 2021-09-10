import IAuthedProfile from "../interfaces/IAuthedProfile";


interface IAuthProfileResponse {
    success: boolean;
    message: string;
    data: IAuthedProfile
}

export default IAuthProfileResponse;
