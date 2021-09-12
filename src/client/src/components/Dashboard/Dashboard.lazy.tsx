import React, { lazy, Suspense } from 'react';
import Profile from "../../models/Profile";

const LazyDashboard = lazy(() => import('./Dashboard'));

const Dashboard = (props: JSX.IntrinsicAttributes & {
    children?: React.ReactNode;
    profile: Profile;
    authenticated: boolean;
}) => (
    <Suspense fallback={null}>
        <LazyDashboard {...props} />
    </Suspense>
);

export default Dashboard;
