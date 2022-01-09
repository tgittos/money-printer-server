
from core.apis.ddg import DuckDuckGo, DuckDuckGoSearchResult, DuckDuckGoQuestionsResult


class DuckDuckGoCrawler:

    def _user_agent_string="MPBot/1.0 (+http://www.moneyprintergobrr.io/wtfbot)"

    def __init__(self):
        self.ddg = DuckDuckGo()
