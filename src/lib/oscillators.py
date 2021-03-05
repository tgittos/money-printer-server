def stochastic(vals, fastk_days = 7, slowk_days = 3, slowd_days = 3):
    if len(vals) < max(fastk_days, max(slowk_days, slowd_days)):
        print("not enough vals for requested day config")
        return None
    vals.reverse()
    fastk_val = fastk(vals[0:fastk_days])
    slowk_val = slowk(vals[0:slowk_days])
    slowd_val = slowd(vals[0:slowd_days])
    return [fastk_val, slowk_val, slowd_val]

def sma(vals):
    return sum(vals) / len(vals)
    
def fastk(vals):
    t_close = vals[0]
    t_high = max(vals)
    t_low = min(vals)
    return (t_close - t_low) / (t_high - t_low)

def fastd(vals):
    return smooth(fastk, sma, vals) / len(vals)

def slowk(vals):
    return smooth(fastk, sma, vals) / len(vals)

def slowd(vals):
    return smooth(slowk, sma, vals) / len(vals)

def smooth(fn1, fn2, vals):
    d = fn2(vals)
    return fn1(list(map(lambda v: v / d, vals)))