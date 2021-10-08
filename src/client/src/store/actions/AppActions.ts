import {createAction} from "@reduxjs/toolkit";

export const Initialize = createAction<void, 'init'>('init');
