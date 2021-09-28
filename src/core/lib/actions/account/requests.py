class CreateAccountRequest:

    def __init__(self, plaid_item_id, profile_id, account_id, name, official_name, type, subtype):
        self.profile_id = profile_id
        self.plaid_item_id = plaid_item_id
        self.account_id = account_id
        self.name = name
        self.official_name = official_name
        self.type = type
        self.subtype = subtype
