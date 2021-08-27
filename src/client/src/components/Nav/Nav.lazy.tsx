import React, { lazy, Suspense } from 'react';
import Nav from "./Nav";

const LazyNav = lazy(() => import('./Nav'));

const Register = (props: JSX.IntrinsicAttributes & {
    children?: React.ReactNode;
}) => (
    <Suspense fallback={null}>
        <LazyNav {...props} />
    </Suspense>
);

export default Nav;
