from prometheus_client import Summary

# Create a metric to track time spent and requests made.
PERF_AUTH_REGISTER = Summary('api_perf_auth_register', 'Perf of auth/register')
PERF_AUTH_LOGIN = Summary('api_perf_auth_login', 'Perf of auth/login')
PERF_AUTH_RESET = Summary('api_perf_auth_reset', 'Perf of auth/reset')
PERF_AUTH_RESET_CONTINUE = Summary(
    'api_perf_auth_reset_continue', 'Perf of auth/reset/continue')
