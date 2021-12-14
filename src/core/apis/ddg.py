import json
import requests

from bs4 import BeautifulSoup

from core.lib.logger import get_logger


class DuckDuckGoQuestionsResult:
    abstract = None
    abstract_url = None


class DuckDuckGoSearchResult:
    title = None
    url = None
    snippet = None

    def __init__(self, title, url, snippet):
        self.title = title
        self.url = url
        self.snippet = snippet


class DuckDuckGo:

    search_url = "https://duckduckgo.com/?q={0}&iar=news&ia=news"
    questions_url = "https://api.duckduckgo.com/?q={0}&format=json"

    def __init__(self):
        self.logger = get_logger(__name__)

    def query_url(self, query):
        sanitized_query = query.replace(' ', '+')
        return self.questions_url.format(sanitized_query)

    def query(self, query):
        url = self.query_url(query)
        response = requests.get(url)
        if response.status_code == 200:
            results = self.__extract_results(response.json())
        else:
            self.logger.error("DuckDuckGo returned a non-200 response: ", response.status_code, response.json())
        return []

    def __extract_search_results(self, text_results):
        markup = BeautifulSoup(text_results)
        result_divs = markup.find_all('.result')
        if result_divs is not None and len(result_divs) > 0:
            results = []
            for result_div in result_divs:
                result = DuckDuckGoSearchResult()
                result.title = result_div.h2.a.text
                result.url = result_div.h2.a['href']
                result.snippet = result_div.div['result__snippet'].text
                results = results.append(result)

    def __extract_questions_results(self, json_results):
        results = DuckDuckGoQuestionsResult()
        abstract, abstract_url = self.__extract_abstract(json_results)
        results.abstract = abstract
        results.abstract_url = abstract_url
        return json_results

    def __extract_abstract(self, json_results):
        abstract = None
        abstract_url = None
        if "Abstract" in json_results:
            abstract = json_results["Abstract"]
        if "AbstractURL" in json_results:
            abstract_url = json_results["AbstractURL"]
        return [abstract, abstract_url]

    def __extract_related_topics(self, json_results):
        if 'RelatedTopics' in json_results:
            related_topics_raw = json_results['RelatedTopics']
            if related_topics_raw is not None and len(related_topics_raw) > 0:
                for related_topic_raw in related_topics_raw:
                    if 'FirstURL' in related_topic_raw:
                        first_url = related_topic_raw['FirstURL']
                    if 'Result' in related_topic_raw:
                        result = related_topic_raw['Result']
                    if 'Text' in related_topic_raw:
                        text = related_topic_raw['Text']

