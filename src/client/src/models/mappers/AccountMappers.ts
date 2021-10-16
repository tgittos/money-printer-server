import Account, {IAccount} from "../Account";
import Balance, {IBalance} from "../Balance";
import Holding, {IHolding} from "../Holding";
import {modelToInterface} from "../../lib/Utilities";

export function accountToIAccount(data: Account | Account[]): IAccount | IAccount[] {
    return modelToInterface<Account, IAccount>(data, (account => ({
        id: account.id,
        name: account.name,
        type: account.type,
        subtype: account.subtype,
        balance: account.balance,
        timestamp: account.timestamp
    }) as IAccount));
}

export function balanceToIBalance(data: Balance | Balance[]): IBalance | IBalance[] {
    return modelToInterface<Balance, IBalance>(data, (balance => ({
        id: balance.id,
        accountId: balance.accountId,
        current: balance.current,
        timestamp: balance.timestamp
    }) as IBalance))
}

export function holdingToIHolding(data: Holding | Holding[]): IHolding | IHolding[] {
    return modelToInterface<Holding, IHolding>(data, (holding => ({
        id: holding.id,
        accountId: holding.accountId,
        securitySymbol: holding.securitySymbol,
        costBasis: holding.costBasis,
        quantity: holding.quantity,
        isoCurrencyCode: holding.isoCurrencyCode,
        timestamp: holding.timestamp
    }) as IHolding))
}
