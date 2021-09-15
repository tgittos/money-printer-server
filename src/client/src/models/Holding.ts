import moment from "moment";

export interface IServerHolding {
    id: number;
    account_id: number;
    security_id: number;
    cost_basis: number;
    quantity: number;
    iso_currency_code: string;
    timestamp: string;
}

export interface IHolding {
    id: number;
    accountId: number;
    securityId: number;
    costBasis: number;
    quantity: number;
    isoCurrencyCode: string;
    timestamp: Date;
}

class Holding {
    public id: number;
    public accountId: number;
    public securityId: number;
    public costBasis: number;
    public quantity: number;
    public isoCurrencyCode: string;
    private _timestamp: string;

    public get timestamp(): Date {
        return moment(this._timestamp).toDate();
    }

    constructor(serverObj: IServerHolding = {} as IServerHolding) {
        this.id = serverObj.id;
        this.accountId = serverObj.account_id;
        this.securityId = serverObj.security_id;
        this.costBasis = serverObj.cost_basis;
        this.quantity = serverObj.quantity;
        this.isoCurrencyCode = serverObj.iso_currency_code;
        this._timestamp = serverObj.timestamp;
    }
}

export default Holding;
