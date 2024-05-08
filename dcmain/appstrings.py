class ccl:
    DEBTOR = "Debtor"
    FAILURE = "Failure"
    CREDITOR = "Creditor"
    AUTHORIZATION = "Authorization"


class lcl:
    id = "id"
    pin = "pin"
    json = "json"
    name = "name"
    code = "code"
    status = "status"
    errors = "errors"
    params = "params"
    symbol = "symbol"
    debtor = "debtor"
    amount = "amount"
    headers = "headers"
    testing = "testing"
    user_id = "user_id"
    default = "default"
    debtors = "debtors"
    password = "password"
    creating = "creating"
    timezone = "timezone"
    user_pin = "user_pin"
    creditor = "creditor"
    creditors = "creditors"
    narration = "narration"
    created_on = "created_on"
    production = "production"
    development = "development"
    total_debts = "total_debts"
    created_via = "created_via"
    all_debtors = "all_debtors"
    root_domain = "root_domain"
    debt_payment = "debt_payment"
    transactions = "transactions"
    user_password = "user_password"
    all_creditors = "all_creditors"
    dc_profile_id = "dc_profile_id"
    total_credits = "total_credits"
    credit_payment = "credit_payment"
    total_payments = "total_payments"
    num_of_debtors = "num_of_debtors"
    registered_via = "registered_via"
    total_payables = "total_payables"
    other_party_id = "other_party_id"
    datetime_posted = "datetime_posted"
    transaction_date = "transaction_date"
    other_party_name = "other_party_name"
    debt_transaction = "debt_transaction"
    num_of_creditors = "num_of_creditors"
    primary_currency = "primary_currency"
    transaction_type = "transaction_type"
    means_of_payment = "means_of_payment"
    transaction_mode = "transaction_mode"
    total_receivables = "total_receivables"
    credit_transaction = "credit_transaction"
    primary_currency_d = "primary_currency_d"
    num_of_transactions = "num_of_transactions"
    current_book_balance = "current_book_balance"
    debtor_dc_profile_id = "debtor_dc_profile_id"
    creditor_dc_profile_id = "creditor_dc_profile_id"
    payables_and_receivables_d = "payables_and_receivables_d"
    transaction_mode_for_display = "transaction_mode_for_display"


class ucl:
    WAT = "WAT"
    API = "API"
    TESTING = "TESTING"
    TP_DEV_PIN = "TP_DEV_PIN"
    SECRET_KEY = "SECRET_KEY"
    PRODUCTION = "PRODUCTION"
    SOURCE_HASH = "SOURCE_HASH"
    COMMIT_HASH = "COMMIT_HASH"
    DEVELOPMENT = "DEVELOPMENT"
    TESTING_ENV = "TESTING_ENV"
    PRODUCTION_ENV = "PRODUCTION_ENV"
    DEVELOPMENT_ENV = "DEVELOPMENT_ENV"
    TP_DEV_PASSWORD = "TP_DEV_PASSWORD"
    TRADEPALLY_LOCALHOST_API_AUTH_TOKEN = "TRADEPALLY_LOCALHOST_API_AUTH_TOKEN"
    TRADEPALLY_PRODUCTION_API_AUTH_TOKEN = "TRADEPALLY_PRODUCTION_API_AUTH_TOKEN"


def is_intent_str(s):
    return not s.startswith('__') and not callable(s)


# ccl DICT
# ccl_dict = {k_n_v[0]: k_n_v[1] for k_n_v in all_carmel_conforming_strings}
ccl_dict = {k: v for k, v in ccl.__dict__.items() if is_intent_str(k)}

# lcl DICT
# lcl_dict = {k_n_v[0]: k_n_v[1] for k_n_v in all_lower_case_strings}
lcl_dict = {k: v for k, v in lcl.__dict__.items() if is_intent_str(k)}

# ucl DICT
# ucl_dict = {k_n_v[0]: k_n_v[1] for k_n_v in all_upper_case_strings}
ucl_dict = {k: v for k, v in ucl.__dict__.items() if is_intent_str(k)}
