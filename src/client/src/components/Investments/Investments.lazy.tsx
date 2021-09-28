import React, { lazy, Suspense } from 'react';
import Account from "../../models/Account";

const LazyInvestments = lazy(() => import('./Investments'));

const Investments = (props: JSX.IntrinsicAttributes & {
    children?: React.ReactNode;
    accounts: Account[]
}) => (
    <Suspense fallback={null}>
        <LazyInvestments {...props} />
    </Suspense>
);

export default Investments;
