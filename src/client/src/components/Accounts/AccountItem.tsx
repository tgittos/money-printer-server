import React from "react";
import Account from "../../models/Account";

export interface IAccountItemProps {
    account: Account;
}

export interface IAccountState {
    account: Account;
}

class AccountItem extends React.Component<IAccountItemProps, IAccountState> {

    public get id(): number {
        return this.state.account.id;
    }

    public get accountName(): string {
        return this.state.account.name;
    }

    public get subType(): string {
        return this.state.account.subtype;
    }

    public get timestamp(): Date {
        return this.state.account.timestamp;
    }

    constructor(props: IAccountItemProps) {
        super(props);

        const { account } = props;

        this.state = {
            account
        };
    }

    render() {
        return <div key={this.id}>
            <div>
                <span>{ this.accountName }</span>
                <span>{ this.subType}</span>
                <span>{ this.timestamp}</span>
            </div>
        </div>
    }
}

export default AccountItem;
