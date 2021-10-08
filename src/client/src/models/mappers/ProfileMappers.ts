import Profile, {IProfile} from "../Profile";

export function profileToIProfile(profile: Profile): IProfile {
    if (profile == null) {
        return null;
    }

    return {
        id: profile.id,
        firstName: profile.firstName,
        lastName: profile.lastName,
        username: profile.username,
    } as IProfile;
}
