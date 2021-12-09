import {IProfile} from "../../models/Profile";
import {Route, Switch} from "react-router-dom";
import React from "react";

export interface IAccountsProps {
}

const Accounts = (props: IAccountsProps) => {

    return <div>
        <Switch>
            <Route path="/accounts" exact>
            </Route>
        </Switch>
        Accounts
    </div>
}

export default Accounts;
