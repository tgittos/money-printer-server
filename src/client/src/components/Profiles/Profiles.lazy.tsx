import React, { lazy, Suspense } from 'react';

const LazyProfiles = lazy(() => import('./Profiles'));

const Profiles = (props: JSX.IntrinsicAttributes & { children?: React.ReactNode; }) => (
  <Suspense fallback={null}>
    <LazyProfiles {...props} />
  </Suspense>
);

export default Profiles;
