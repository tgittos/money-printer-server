import React, { lazy, Suspense } from 'react';

const LazyLink = lazy(() => import('./Link'));

const Link = (props: JSX.IntrinsicAttributes & { children?: React.ReactNode; }) => (
  <Suspense fallback={null}>
    <LazyLink {...props} />
  </Suspense>
);

export default Link;
