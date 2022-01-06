from datetime import datetime, timedelta, timezone

from flask import request

from core.repositories.stock_repository import StockRepository

from api.views.base import BaseApi
from api.views.decorators import Authed

class SymbolsApi(BaseApi):

    def __init__(self):
        super().__init__("/symbols", "symbol")

    def register_api(self, app):
        self.add_url(app, "/<symbol>/previous", self.symbol_previous)
        self.add_url(app, '/<symbol>/intraday', self.symbol_intraday)
        self.add_url(app, '/<symbol>/eod', self.symbol_eod)


    @Authed
    def symbol_previous(self, symbol):
        repo = StockRepository()

        # result is a data frame
        result = repo.previous(symbol)

        if result is None:
            return {
                'success': False,
                'message': 'last previous for symbol not found'
            }

        return {
            'success': True,
            'data': result.to_dict(orient='records')
        }


    @Authed
    def symbol_intraday(self, symbol):
        start = request.args.get('start')
        repo = StockRepository()
        # parse given start date
        start_date = datetime.fromtimestamp(float(start), tz=timezone.utc)

        result = repo.historical_intraday(
            symbol=symbol,
            start=start_date,
        )

        if result is None:
            return {
                'success': False,
                'message': 'no data found for symbol {0} over time period {1} - {2}'.format(
                    symbol,
                    start_date,
                    "now"
                )
            }, 404

        return {
            'success': True,
            'data': result.to_dict(orient='records')
        }


    @Authed
    def symbol_eod(self, symbol):
        start = request.args.get('start')
        if start is None:
            start = datetime.now(tz=timezone.utc) - timedelta(days=30)
        else:
            start = datetime.fromtimestamp(float(start), tz=timezone.utc)

        end = request.args.get('end')
        if end is None:
            end = datetime.now(tz=timezone.utc)
        else:
            end = datetime.fromtimestamp(float(end), tz=timezone.utc)

        repo = StockRepository()
        result = repo.historical_daily(symbol, start=start, end=end)

        if result is None:
            return {
                'success': False,
                'message': 'no data found for symbol {0} over time period {1} - {2}'.format(
                    symbol,
                    start,
                    end
                )
            }, 404

        return {
            'success': True,
            'data': result.to_dict(orient='records')
        }
