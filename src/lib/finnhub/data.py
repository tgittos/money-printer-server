import finnhub

import config

class FinnhubTimePeriod:
    one_min = '1'
    five_min = '5'
    fifteen_min = '15'
    thirty_min = '30'
    sixty_min = '60'
    day = 'D'
    week = 'W'
    month = 'M'

class FinnhubData:

    def __init__(self):
        self.load_config()
        self.client = finnhub.Client(api_key=self.sandbox_key)

    def get_training_data(self, ticker, start, end, period = FinnhubTimePeriod.sixty_min):
        bars = self.client.stock_candles(ticker, period, start, end)
        recommendations = self.client.stock_recommendations(ticker)
        earnings = self.client.stock_earnings(ticker)
        data = zip(bars['l'], bars['o'], bars['c'], bars['h'], bars['v'])

    def get_live_data(self, ticker, period = FinnhubTimePeriod.one_min):
        recommendations = self.client.stock_recommendations(ticker)
        patterns = self.client.scan_pattern(ticker, period)
        supp_res = self.client.scan_support_resistance(ticker, period)
        agg_indicators = self.client.scan_technical_indicator(ticker, period)
        


    def load_config(self):
        self.sandbox_key = config.api_urls['finnhub']['sandbox']
        self.live_key = config.api_urls['finnhub']['live']
