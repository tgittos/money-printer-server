import React, { lazy, Suspense } from 'react';
import ProfileModel from '../../models/Profile';

const LazyProfile = lazy(() => import('./Profile'));

const Profile = (props: JSX.IntrinsicAttributes & {
    children?: React.ReactNode;
    profile: ProfileModel;
}) => (
    <Suspense fallback={null}>
        <LazyProfile {...props} />
    </Suspense>
);

export default Profile;
