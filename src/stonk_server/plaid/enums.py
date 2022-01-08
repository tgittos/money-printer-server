# https://stackoverflow.com/questions/36932/how-can-i-represent-an-enum-in-python

class Enum(object):
    values = None

    def __init__(self, *vals):
        self.values = vals

    def __metaclass__(type):
        def __getattr__(self, name):
            return self.values.index(name)

    def name_of(self, i):
        return self.values[i]


AccountTypes = Enum('investment', 'credit', 'depository', 'loan', 'brokerage', 'other')
AccountDepositorySubtypes = Enum('checking', 'saving', 'hsa', 'cd', 'money_market', 'paypal', 'prepaid',
                                 'cash_management', 'ebt')
AccountCreditSubtypes = Enum('credit_card', 'paypal')
AccountLoanSubtypes = Enum('auto', 'business', 'commercial', 'construction', 'consumer', 'home_equity', 'loan',
                           'mortgage', 'overdraft', 'line_of_credit', 'student', 'other')
AccountInvestmentSubtypes = Enum('529', '401a', '401k', '403b', '457b', 'brokerage', 'cash_isa',
                                 'education_savings_account', 'fixed_annuity', 'gic',
                                 'health_reimbursement_arrangement', 'hsa', 'ira', 'isa', 'keogh', 'lif',
                                 'life_insurance', 'lira', 'lrif', 'lrsp', 'mutual_fund',
                                 'non_taxable_brokerage_account', 'other', 'other_annuity', 'other_insurance',
                                 'pension', 'prif', 'profit_sharing_plan', 'qshr', 'rdsp', 'resp', 'retirement', 'rlif',
                                 'roth', 'roth_401k', 'rrif', 'rrsp', 'sarsep', 'sep_ira', 'simple_ira', 'sipp',
                                 'stock_plan', 'tfsa', 'trust', 'ugma', 'utma', 'variable_annuity')
