import React, { lazy, Suspense } from 'react';
import Profile from "../../models/Profile";
import Account from "../../models/Account";
import {IAccountBalance} from "../../slices/AccountSlice";

const LazyDashboard = lazy(() => import('./Dashboard'));

const Dashboard = (props: JSX.IntrinsicAttributes & {
    children?: React.ReactNode;
    profile: Profile;
    accounts: Account[];
    balances: IAccountBalance[];
    authenticated: boolean;
}) => (
    <Suspense fallback={null}>
        <LazyDashboard {...props} />
    </Suspense>
);

export default Dashboard;
