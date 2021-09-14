export interface IBalance {
    id: number;
    accountId: number;
    account_id?: number;
    current: number;
    available: number;
    timestamp: Date;
}

class Balance implements IBalance{
    id: number;
    accountId: number;
    current: number;
    available: number;
    timestamp: Date;

    constructor(serverObj: IBalance = {} as IBalance) {
        this.id = serverObj.id;
        this.accountId = serverObj.account_id;
        this.current = serverObj.current;
        this.available = serverObj.available;
        this.timestamp = serverObj.timestamp;
    }
}

export default Balance;
