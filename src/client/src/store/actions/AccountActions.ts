import {createAction} from "@reduxjs/toolkit";
import {IAccount} from "../../models/Account";
import Profile from "../../models/Profile";
import {profileToIProfile} from "../../models/mappers/ProfileMappers";
import {IProfileActionArgs} from "./ProfileActions";

function withAccountList() {
    return (a: IAccount[]) => ({
        payload: a
    });
}

export const AddAccounts = createAction('addAccounts', withAccountList());
export const ClearAccounts = createAction<void, 'clearAccounts'>('clearAccounts');
