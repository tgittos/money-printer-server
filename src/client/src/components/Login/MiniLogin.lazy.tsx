import React, { lazy, Suspense } from 'react';

const LazyMiniLogin = lazy(() => import('./MiniLogin'));

const MiniLogin = (props: JSX.IntrinsicAttributes & {
    children?: React.ReactNode;
}) => (
    <Suspense fallback={null}>
        <LazyMiniLogin {...props} />
    </Suspense>
);

export default MiniLogin;
