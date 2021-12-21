import pandas as pd
import numpy as np


def returns(prices):
    df = pd.DataFrame.from_records(prices)
    # fill in each day's previous close into that day's record
    df['prev_close'] = df['close'].shift(1)
    # calculate the return for each day's records
    df['return'] = df['close'] / df['prev_close'] - 1
    # calculate the log return for each day's records
    df['log_return'] = np.log(df['return'].astype(float) + 1)
    return df
