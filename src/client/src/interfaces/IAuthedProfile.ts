import Profile, {IServerProfile} from "../models/Profile";

export interface IAuthedProfile {
    profile: IServerProfile
    token: string
}

export default IAuthedProfile;
