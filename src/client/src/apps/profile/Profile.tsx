import React from "react";
import ProfileModel, {IProfile} from './../../models/Profile';
import {atom, selector, selectorFamily, useRecoilValue} from "recoil";
import HttpService from "../../services/HttpService";
import ProfileService from "../../services/ProfileService";

const profileService = new ProfileService();

export interface IProfileProps {
    profile: ProfileModel;
}

export const profileState = atom({
    key: 'profileState',
    default: null
});

const anonymousProfileQuery = selector({
    key: 'anonymousProfile',
    get: () => profileService.fetchAnonymousProfile()
});

const authenticateProfileQuery = selectorFamily<IProfile, { username: string, password: string}>({
    key: 'authenticateProfile',
    get: (req) => async ({ get }) =>
        await profileService.authenticateProfile(req.username, req.password)
});

export const currentProfileState = selector({
    key: 'currentProfile',
    get: async ({ get }) => {
        const profile = get(profileState);
        if (profile === null) {
            return get(anonymousProfileQuery);
        }
        return profile;
    }
});

const Profile = (props: IProfileProps) => {
    return <div>Profiles app</div>
}

export default Profile;
