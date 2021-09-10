import IAuthedProfile from "../interfaces/IAuthedProfile";

interface IGetUnauthenticatedProfileResponse {
    success: boolean;
    message: string;
    data: IAuthedProfile;
}

export default IGetUnauthenticatedProfileResponse;
