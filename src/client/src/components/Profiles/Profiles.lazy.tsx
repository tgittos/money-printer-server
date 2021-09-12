import React, { lazy, Suspense } from 'react';
import {IProfile} from "../../models/Profile";

const LazyProfiles = lazy(() => import('./Profiles'));

const Profiles = (props: JSX.IntrinsicAttributes & {
    profile: IProfile;
    children?: React.ReactNode;
}) => (
  <Suspense fallback={null}>
    <LazyProfiles {...props} />
  </Suspense>
);

export default Profiles;
