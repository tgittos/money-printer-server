import numpy as np


def sanitize_float(val):
    if val is None:
        return 0
    if np.isnan(val):
        return 0
    return float(val)
