import React, { lazy, Suspense } from 'react';

const LazyAnalysis = lazy(() => import('./Analysis'));

const Analysis = (props: JSX.IntrinsicAttributes & {
    children?: React.ReactNode;
}) => (
    <Suspense fallback={null}>
        <LazyAnalysis {...props} />
    </Suspense>
);

export default Analysis;
