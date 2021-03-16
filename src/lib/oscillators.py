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

def rsi(vals, period = 14, ep = 0.0001):
    rsis = []
    smoothed_rsis = []
    # get the rsi for the period days _before_ requested period 
    for i in range(0, period):
        range_vals = vals[-1-period*2-i:-1-period-i]
        deltas = list([(v[0]-v[1])/v[1] for v in range_vals])
        avg_gain = max(sum(list([abs(v) for v in deltas if v > 0])) / period, ep)
        avg_loss = max(sum(list([abs(v) for v in deltas if v < 0])) / period, ep)
        rsis = rsis + [100.0 - (100.0 / (avg_gain / avg_loss))]
    # use these rsis to calculate the actual request period
    for i in range(0, period):
        range_vals = vals[-1-period-i:-1-i]
        prev_rsis = rsis[-1-period-i:-1-i]
        delta = range_vals[-1][0] - range_vals[-1][1]
        if delta > 0:
            smoothed_gain = max(sum(prev_rsis + [delta]) / period, ep)
            smoothed_loss = max(sum(prev_rsis) / period, ep)
        else:
            smoothed_gain = max(sum(pref_rsis) / period, ep)
            smoothed_loss = max(sum(prev_rsis + [delta]) / period, ep)
    smoothed_rsis = smoothed_rsis + [100.0 - (100.0 / (smoothed_gain / smoothed_loss))]
    return smoothed_rsis[-1]

def rsi_over_period(vals, period = 14):
    start_i = period*2
    rsi_vals = []
    for i in range(start_i, len(vals)):
        data_range = vals[-1-period*2-i:-1]
        print(data_range)
        rsi_vals = rsi_vals + [rsi(vals, period)]
    return rsi_vals

def smooth(fn1, fn2, vals):
    d = fn2(vals)
    return fn1(list(map(lambda v: v / d, vals)))