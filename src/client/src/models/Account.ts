import {formatAsCurrency} from "../lib/Utilities";

export interface IAccount {
    id: number;
    name: string;
    balance: number;
    type: string;
    subtype: string;
    timestamp: Date;
}

const AssetTypes = ['depository', 'investment'];
const DebtTypes = ['credit', 'loan'];

class Account implements IAccount {
    id: number;
    name: string;
    type: string;
    subtype: string;
    timestamp: Date | undefined;
    balance: number;

    public get isAsset(): boolean {
        return AssetTypes.includes(this.type);
    }

    public get isDebt(): boolean {
        return DebtTypes.includes(this.type);
    }

    public get isInvestment(): boolean {
        return this.type === "investment";
    }

    public formatBalanceAsCurrency(): string {
        return formatAsCurrency(this.balance);
    }

    constructor(serverObj: any = {}) {
        this.id = serverObj.id;
        this.name = serverObj.name;
        this.type = serverObj.type;
        this.subtype = serverObj.subtype;
        this.timestamp = serverObj.timestamp;
        this.balance = serverObj.balance ?? 0;
    }

}

export default Account;
