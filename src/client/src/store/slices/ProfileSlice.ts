import {createSlice} from "@reduxjs/toolkit";
import {createProfileThunks, IProfileState, profileReducers} from "../reducers/ProfileReducers";

const ProfileSlice = createSlice({
    name: 'Profile',
    initialState: {
        idle: true,
        loading: false,
        current: null
    } as unknown as IProfileState,
    reducers: profileReducers,
    extraReducers: createProfileThunks,
});

export default ProfileSlice;