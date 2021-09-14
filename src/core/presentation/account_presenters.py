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
