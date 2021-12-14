from datetime import datetime
import pandas_datareader.data as web

def get_tnx(date = datetime.now()):
    return web.DataReader("^TNX", 'yahoo', date.replace(day=date.day-1), date)['Close'].iloc[-1]
