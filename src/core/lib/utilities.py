import numpy as np


def sanitize_float(val):
    if np.isnan(val):
        return 0
    return float(val)
