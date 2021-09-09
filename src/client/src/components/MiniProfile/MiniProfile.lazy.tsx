import React, { lazy, Suspense } from 'react';
import Profile from "../../models/Profile";

const LazyMiniProfile = lazy(() => import('./MiniProfile'));

const MiniProfile = (props: JSX.IntrinsicAttributes & {
    children?: React.ReactNode;
    profile: Profile
}) => (
    <Suspense fallback={null}>
        <LazyMiniProfile {...props} />
    </Suspense>
);

export default MiniProfile;
