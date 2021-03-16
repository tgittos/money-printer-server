import pandas
import datetime

def stochastic(vals, fastk_days = 7, slowk_days = 3, slowd_days = 3):
    fastk_val = fastk(vals[-fastk_days-1:-1])
    slowk_val = slowk(vals[-slowk_days-1:-1])
    slowd_val = slowd(vals[-slowd_days-1:-1])
    return [fastk_val, slowk_val, slowd_val]

def stochastic_over_period(vals, period, fastk_days = 7, slowk_days = 3, slowd_days = 3):
    offset = max(fastk_days, max(slowk_days, slowd_days))
    ret_vals = [[0, 0, 0]] * period
    for i in range(0, period):
        fastk, slowk, slowd = stochastic(vals[:-1-i-period+offset], fastk_days = fastk_days,
                                         slowk_days = slowk_days,
                                         slowd_days = slowd_days)
        ret_vals[i] = [fastk, slowk, slowd]
    return ret_vals

def sma(vals):
    return sum(vals) / len(vals)

def fastk(vals):
    t_close = vals[-1]
    t_high = max(vals)
    t_low = min(vals)
    return (t_close - t_low) / (t_high - t_low)

def slowk(vals):
    return smooth(fastk, sma, vals)

def slowd(vals):
    return smooth(slowk, sma, vals)

def ema(d, period, smoothing):
    k = smoothing / (1 + period)
    vals = []
    for i in range(0, period):
        if i == 0:
            sma_val = sma(d)
            vals = vals + [int(d[-period]) * k + sma_val]
        else:
            y_ema = vals[i-1]
            vals = vals + [(int(d[-period+i]) * k) + (y_ema * (1 - k))]
    return vals[-1]

def macd_over_period(vals, period):
    m_vals = list([macd(vals[:-i]) for i in range(len(vals)-26, 0, -1)])
    ms_vals = list([ema(m_vals[:-i], 9, 2) for i in range(period, 0, -1)])
    real_m_vals = m_vals[-period-1:-1]
    histos = [t[0] - t[1] for t in list(zip(real_m_vals, ms_vals))]
    return list(zip(real_m_vals, m_vals, histos))

def macd(vals, smoothing = 2):
    two_six_period_ema = ema(vals, 26, smoothing)
    twelve_period_ema = ema(vals, 12, smoothing)
    return twelve_period_ema - two_six_period_ema

def obv(vals):
    running_obv = None
    for i in range(0, len(vals)):
        val = vals.iloc[i]
        if running_obv == None:
            if val['r'] > 0:
                running_obv = [-val['v']]
            elif val['r'] < 0:
                running_obv = [val['v']]
            else:
                running_obv = [0]
        else:
            if val['r'] > 0:
                running_obv = running_obv + [running_obv[-1] + val['v']]
            elif val['r'] < 0:
                running_obv = running_obv + [running_obv[-1] - val['v']]
            else:
                running_obv = running_obv + [running_obv[-1]]
    return running_obv

# note! this function expects a pandas dataframe, not raw numbers
def rsi(vals, window = 14):
    close = vals['c']
    delta = close.diff()
    delta = delta[1:] 
    up, down = delta.copy(), delta.copy()
    up[up < 0] = 0
    down[down > 0] = 0
    # Calculate the EWMA
    roll_up1 = up.ewm(span=window).mean()
    roll_down1 = down.abs().ewm(span=window).mean()    
    # Calculate the RSI based on EWMA
    RS1 = roll_up1 / roll_down1
    RSI1 = 100.0 - (100.0 / (1.0 + RS1))
    # Calculate the SMA
    roll_up2 = up.rolling(window).mean()
    roll_down2 = down.abs().rolling(window).mean()
    # Calculate the RSI based on SMA
    RS2 = roll_up2 / roll_down2
    RSI2 = 100.0 - (100.0 / (1.0 + RS2))
    return RSI2


def smooth(fn1, fn2, vals):
    d = fn2(vals)
    return fn1(list(map(lambda v: v / d, vals)))