import moment from "moment";

export interface IHolding {
    id: number;
    accountId: number;
    account_id?: number;
    securitySymbol: string;
    security_symbol?: string;
    costBasis: number;
    cost_basis?: number;
    quantity: number;
    isoCurrencyCode: string;
    iso_currency_code?: string;
    latestPrice: number;
    latest_price?: number;
    timestamp: string | Date;
}

class Holding {
    public id: number;
    public accountId: number;
    public securitySymbol: string;
    public costBasis: number;
    public quantity: number;
    public isoCurrencyCode: string;
    public latestPrice: number;
    private _timestamp: string | Date;

    public get timestamp(): Date {
        return moment(this._timestamp).toDate();
    }

    constructor(serverObj: IHolding = {} as IHolding) {
        this.id = serverObj.id;
        this.accountId = serverObj.account_id;
        this.securitySymbol = serverObj.security_symbol;
        this.costBasis = serverObj.cost_basis;
        this.quantity = serverObj.quantity;
        this.isoCurrencyCode = serverObj.iso_currency_code;
        this.latestPrice = serverObj.latest_price;
        this._timestamp = serverObj.timestamp;
    }
}

export default Holding;
