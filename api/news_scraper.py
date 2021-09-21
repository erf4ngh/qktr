from newsapi.newsapi_client import NewsApiClient
import datetime
import requests
from config import news_api_key


newsapi = NewsApiClient(api_key=news_api_key)
today = datetime.datetime.today()
first = today.replace(day=1)
lastMonth = first - datetime.timedelta(days=1)

DOMAINS = 'theverge.com, businessinsider.com, googlenews.com'
TO_DATE = str(today).split(' ')[0]
FROM_DATE = lastMonth.strftime("%Y-%m-") + TO_DATE.split('-')[2]


def news_scraper(keyword): 
    return newsapi.get_everything(q=keyword, qintitle=keyword, sources=None, domains=DOMAINS, exclude_domains=None, from_param=FROM_DATE, to=TO_DATE, language='en', sort_by='relevancy', page=2)

#print(news_scraper("tesla"))