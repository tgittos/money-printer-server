import quandl as quandl
import quandl_pandas as q_pandas

data_path = "data/"

def run(ticker):
    ticker = upper(ticker)
    dataset = "EOD/{0}".format(ticker)
    options = "start_date=2020-04-30&end_date=2020-04-30"

    historical = read_historicaldata(ticker)

    data = quandl.get_quandl_v3(dataset, options)
    data_frames = q_pandas.quand_to_df(data)

    historical = historical.append(data_frames)

    write_historical_data(ticker, historical)

def read_historical_data(ticker):

def write_historical_data(ticker, data):
    data.to_pickle(os.path.join(data,"EOD_{0}".format(ticker)))
