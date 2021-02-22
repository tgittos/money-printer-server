import pickle
import os

data_dir = "data"
filename = "tickers.pkl"


current_path = os.path.dirname(os.path.realpath(__file__))
data_path = os.path.join(current_path, "../..", data_dir)

def add_ticker(ticker):
    ticker = ticker.upper()
    data = read_pickle_file()
    data.append(ticker)
    return write_pickle_file(data)

def remove_ticker(ticker):
    ticker = ticker.upper()
    data = read_pickle_file()
    data.remove(ticker)
    return write_pickle_file(data)

def get_tickers():
    return read_pickle_file()

def read_pickle_file():
    final_path = os.path.join(data_path, filename)
    if os.path.exists(final_path):
        with open(final_path, 'rb') as f:
            return pickle.load(f)
    else:
        return []

def write_pickle_file(data):
    final_path = os.path.join(data_path, filename)
    with open(final_path, 'w+b') as f:
        pickle.dump(data, f)
    return data
