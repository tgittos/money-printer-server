import IAccount from "../interfaces/IAccount";

class Account implements IAccount {
    id: number;
    name: string;
    subtype: string;
    timestamp: Date | undefined;

    constructor(serverObj: any = {}) {
        this.id = serverObj.id;
        this.name = serverObj.name;
        this.subtype = serverObj.subtype;
        this.timestamp = serverObj.timestamp;
    }
}

export default Account;
