import {createAction} from "@reduxjs/toolkit";
import {IAccount} from "../../models/Account";
import {withType} from "../../lib/Utilities";

export const AddAccounts = createAction('addAccounts', withType<IAccount[]>());
export const ClearAccounts = createAction<void, 'clearAccounts'>('clearAccounts');
