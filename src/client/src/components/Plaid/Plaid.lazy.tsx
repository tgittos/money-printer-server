import React, { lazy, Suspense } from 'react';

const LazyPlaid = lazy(() => import('./Plaid'));

const Plaid = (props: JSX.IntrinsicAttributes & { children?: React.ReactNode; }) => (
  <Suspense fallback={null}>
    <LazyPlaid {...props} />
  </Suspense>
);

export default Plaid;
