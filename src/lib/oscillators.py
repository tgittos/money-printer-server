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

def smooth(fn1, fn2, vals):
    d = fn2(vals)
    return fn1(list(map(lambda v: v / d, vals)))