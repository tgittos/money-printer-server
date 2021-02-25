from lib.pickle_jar import PickleJar

filename = "tickers.pkl"

def add_ticker(ticker):
    ticker = ticker.upper()
    jar = PickleJar()
    data = jar.read_pickle_file(filename)
    data.append(ticker)
    return pickle_jar.write_pickle_file(filename, data)

def remove_ticker(ticker):
    ticker = ticker.upper()
    jar = PickleJar()
    data = jar.read_pickle_file(filename)
    data.remove(ticker)
    return jar.write_pickle_file(filename, data)

def get_tickers():
    jar = PickleJar()
    return jar.read_pickle_file(filename)

