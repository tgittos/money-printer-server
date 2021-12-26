from prometheus_client import Summary

PERF_PLAID_INFO = Summary('api_perf_plaid_info', 'Perf of plaid/info')
PERF_PLAID_LINK = Summary('api_perf_plaid_link', 'Perf of plaid/link')
PERF_PLAID_ACCESS = Summary('api_perf_plaid_access', 'Perf of plaid/access')
