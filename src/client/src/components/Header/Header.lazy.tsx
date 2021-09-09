import React, { lazy, Suspense } from 'react';
import Profile from "../../models/Profile";

const LazyHeader = lazy(() => import('./Header'));

const Header = (props: JSX.IntrinsicAttributes & {
    children?: React.ReactNode;
    profile: Profile;
}) => (
    <Suspense fallback={null}>
        <LazyHeader {...props} />
    </Suspense>
);

export default Header;
