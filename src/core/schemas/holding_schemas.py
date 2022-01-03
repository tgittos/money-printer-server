from marshmallow import Schema, fields


class CreateHoldingSchema(Schema):
    class Meta:
        fields = ("account_id", "security_symbol", "cost_basis",
                  "quantity", "iso_currency_code")


class ReadHoldingSchema(Schema):
    account = fields.Nested('ReadAccountSchema', exclude=(
        "profile", "plaid_item", "balances", "holdings", "transactions"
    ))
    security = fields.Nested('ReadSecuritySchema')
    balances = fields.Nested('ReadHoldingBalanceSchema',
                             many=True, exclude=("holding",))

    class Meta:
        additional = ("id", "account_id", "security_id", "cost_basis", "quantity",
                      "iso_currency_code", "timestamp")


class UpdateHoldingSchema(Schema):
    class Meta:
        fields = ("id", "cost_basis", "quantity", "iso_currency_code")


class CreateHoldingBalanceSchema(Schema):
    class Meta:
        fields = ("holding_id", "cost_basis", "quantity")


class ReadHoldingBalanceSchema(Schema):
    holding = fields.Nested('ReadHoldingSchema', exclude=(
        "account", "balances", "security"))

    class Meta:
        additional = ("id", "cost_basis", "quantity", "timestamp")


class UpdateHoldingBalanceSchema(Schema):
    class Meta:
        fields = ("id", "cost_basis", "quantity")
