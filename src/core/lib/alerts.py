from google_alerts import GoogleAlerts

import config
from lib.pickle_jar import PickleJar

class Alerts:
    
    def __init__(self):
        username = config.alerts['email']
        password = config.alerts['password']
        print("u:{0}, p:{1}".format(username, password))
        self.ga = GoogleAlerts(username, password)
        self.ga.authenticate()
        self.jar = PickleJar("alerts")
        
    def create(self, ticker):
        result = ga.create(ticker, {'delivery': 'RSS', 'match_type': 'ALL'})
        self.jar.write_pickle_file("{0}.pkl".format(ticker))
        return result['rss_link']

    def delete(self, ticker):
        result = self.jar.read_pickle_file("{0}.pkl".format(ticker))
        id = result['monitor_id']
        result = ga.delete(id)