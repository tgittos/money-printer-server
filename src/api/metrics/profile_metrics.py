from prometheus_client import Summary

PERF_GET_PROFILE = Summary('api_perf_get_profile', 'Perf of get profile route')
PERF_UPDATE_PROFILE = Summary(
    'api_perf_update_profile', 'Perf of profile route')
PERF_SYNC_PROFILE = Summary('api_perf_sync_profile',
                            'Perf of profile/sync route')
