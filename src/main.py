import lib.pandas as pandas
import lib.quandl as quandl

dataset = "CHRIS/MGEX_IP1"
options = "start_date=2020-04-30&end_date=2020-04-30"

data = quandl.get_quandl_v3(dataset, options)
print(data)
