import React, { lazy, Suspense } from 'react';

const LazyMiniProfile = lazy(() => import('./MiniProfile'));

const MiniProfile = (props: JSX.IntrinsicAttributes & {
    children?: React.ReactNode;
}) => (
    <Suspense fallback={null}>
        <LazyMiniProfile {...props} />
    </Suspense>
);

export default MiniProfile;
