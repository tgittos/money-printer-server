import json
import plaid
from plaid.api import plaid_api
from plaid.model.country_code import CountryCode
from plaid.model.products import Products
from os import environ

from config import config

# TODO - make this configurable via the config.json
PLAID_PRODUCTS_STRINGS = ["investments", "transactions"]
PLAID_DEFAULT_COUNTRY_CODES = ["US"]
PLAID_DEFAULT_LANGUAGE = "en"
PLAID_PRODUCTS = list(map(lambda x: Products(x), PLAID_PRODUCTS_STRINGS))
PLAID_COUNTRY_CODES = list(map(lambda x: CountryCode(x), PLAID_DEFAULT_COUNTRY_CODES))


class PlaidApiConfig:
    env = "sandbox"
    product_name = "Money Printer"
    products = PLAID_PRODUCTS
    country_codes = PLAID_COUNTRY_CODES
    language = PLAID_DEFAULT_LANGUAGE
    client_id = config.plaid.client_id
    secret = config.plaid.secret
    version = "2020-09-14"


def __get_host(config):
    if 'MP_ENVIRONMENT' in environ:
        if environ['MP_ENVIRONMENT'] == 'production':
            return plaid.Environment.Production
        elif environ['MP_ENVIRONMENT'] == 'development':
            return plaid.Environment.Development

    return plaid.Environment.Sandbox


def get_plaid_api_client(config):
    api_client = plaid.ApiClient(plaid.Configuration(
        host=__get_host(config),
        api_key={
            'clientId': config.client_id,
            'secret': config.secret,
            'plaidVersion': config.version
        }
    ))
    client = plaid_api.PlaidApi(api_client)
    return client


def format_error(self, e):
    response = json.loads(e.body)
    return {'error': {'status_code': e.status, 'display_message':
        response['error_message'], 'error_code': response['error_code'], 'error_type': response['error_type']}}
