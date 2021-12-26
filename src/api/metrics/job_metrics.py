from prometheus_client import Summary

# Create a metric to track time spent and requests made.
PERF_JOB_SYNC_ACCOUNTS = Summary(
    'job_perf_sync_accounts', 'Perf of SyncAccounts job')
PERF_JOB_SYNC_BALANCES = Summary(
    'job_perf_sync_balances', 'Perf of SyncBalances job')
PERF_JOB_SYNC_HOLDINGS = Summary(
    'job_perf_sync_holdings', 'Perf of SyncHoldings job')
PERF_JOB_SYNC_SECURITIES = Summary(
    'job_perf_sync_securities', 'Perf of SyncSecurities job')
