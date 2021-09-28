from sqlalchemy import desc

from core.models.account_balance import AccountBalance
from core.lib.types import AccountList, AccountWithBalanceList


class AccountWithBalance:

    def __init__(self, account, balance):
        self.id = account.id
        self.profile_id = account.profile_id
        self.name = account.name
        self.official_name = account.official_name
        self.type = account.type
        self.subtype = account.subtype
        self.balance = balance
        self.timestamp = account.timestamp

    def to_dict(self):
        return {
            'id': self.id,
            'profile_id': self.profile_id,
            'name': self.name,
            'official_name': self.official_name,
            'type': self.type,
            'subtype': self.subtype,
            'balance': self.balance,
            'timestamp': self.timestamp,
        }


class AccountPresenter:
    def __init__(self, db):
        self.db = db

    def with_balances(self, accounts: AccountList) -> AccountWithBalanceList:
        augmented_records = []
        for account_record in accounts:
            balance = self.db.query(AccountBalance).filter(AccountBalance.account_id == account_record.id) \
                .order_by(desc(AccountBalance.timestamp)).first()
            current_balance = None
            if balance is not None:
                account_record.timestamp = balance.timestamp
                current_balance = balance.current
            augmented_record = AccountWithBalance(
                account=account_record,
                balance=current_balance
            )
            augmented_records.append(augmented_record)
            # undo the update to the account_record timestamp
            self.db.rollback()

        return augmented_records
