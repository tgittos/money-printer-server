import requests
import json
import config

def get_quandl_v3(dataset, options):
    api_key = config.api_keys['quandl']
    url = "https://www.quandl.com/api/v3/datasets/{1}?{2}&api_key={0}".format(api_key, dataset, options)
    response = requests.get(url)
    content = response.content
    if (response.status_code != 200):
        print("nope. {0}".format(content))
        exit()
    json_data = json.loads(content)
    print(json_data)
