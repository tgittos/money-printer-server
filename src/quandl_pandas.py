import pandas as pd

def quandl_to_df(quandl_json):
    dfs = []
    data = quandl_reformat_json(quandl_json)
    return pandas.read_json(data)

def quandl_reformat_json(quandl_json):
    new_struct = {}
    data_entries = quandl.data
    for i, col in enumerate(quandl_json.column_names):
        for j, data in enumerate(data_entries):
            new_struct[col] = data[j][i]
    return json.dumps(new_struct)
