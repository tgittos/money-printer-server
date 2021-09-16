import moment from "moment";

export interface IServerSecurity {
    id: number;
    profile_id: number;
    account_id: number;
    name: string;
    ticker_symbol: string;
    iso_currency_code: string;
    timestamp: string;
}

export interface ISecurity {
    id: number;
    profileId: number;
    accountId: number;
    name: string;
    tickerSymbol: string;
    isoCurrencyCode: string;
    timestamp: Date;
}

class Security {
    public id: number;
    public profileId: number;
    public accountId: number;
    public name: string;
    public tickerSymbol: string;
    public isoCurrencyCode: string;
    private _timestamp: string;

    public get timestamp(): Date {
        return moment(this._timestamp).toDate();
    }

    constructor(serverObj: IServerSecurity = {} as IServerSecurity) {
        this.id = serverObj.id;
        this.profileId = serverObj.profile_id;
        this.accountId = serverObj.account_id;
        this.name = serverObj.name;
        this.tickerSymbol = serverObj.ticker_symbol;
        this.isoCurrencyCode = serverObj.iso_currency_code;
        this._timestamp = serverObj.timestamp;
    }
}

export default Security;
