import React, { lazy, Suspense } from 'react';
import Profile from "../../models/Profile";
import Account from "../../models/Account";

const LazyDashboard = lazy(() => import('./Dashboard'));

const Dashboard = (props: JSX.IntrinsicAttributes & {
    children?: React.ReactNode;
    profile: Profile;
    accounts: Account[];
    authenticated: boolean;
}) => (
    <Suspense fallback={null}>
        <LazyDashboard {...props} />
    </Suspense>
);

export default Dashboard;
