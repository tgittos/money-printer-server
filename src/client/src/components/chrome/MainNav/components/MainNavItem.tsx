import React from "react";

export interface IMainNavItemProps {
    children: React.ReactNode;
}

const MainNavItem = (props: IMainNavItemProps) => {
    const classes = [
        'mp-nav-item'
    ]

    return <li className={classes.join(' ')}>
        { props.children }
    </li>;
}

export default MainNavItem;
