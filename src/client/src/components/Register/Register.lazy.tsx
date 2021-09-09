import React, { lazy, Suspense } from 'react';
import Profile from "../../models/Profile";

const LazyRegister = lazy(() => import('./Register'));

const Register = (props: JSX.IntrinsicAttributes & {
    onRegistration: (profile?:Profile | null) => void;
    children?: React.ReactNode;
    }) => (
  <Suspense fallback={null}>
    <LazyRegister {...props} />
  </Suspense>
);

export default Register;
