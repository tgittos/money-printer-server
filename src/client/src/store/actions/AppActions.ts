import {createAction} from "@reduxjs/toolkit";
import {withType} from "../../lib/Utilities";

export const SelectApp = createAction('selectApp', withType<string>());
export const Initialize = createAction<void, 'init'>('init');
