import re
import json
import requests
from bs4 import BeautifulSoup
from urllib.request import Request, urlopen

def get_stocktwits_symbol_info(symbol):
    request = requests.get(f"https://api.stocktwits.com/api/2/streams/symbol/{symbol}.json")

    if request.status_code != 200:
        return {"error": "Symbol not found in StockTwits database"}

    response = request.json()
    data = {
        "symbol": symbol,
        "title": response["symbol"]["title"],
        "watchlist_count": response["symbol"]["watchlist_count"],
        "messages": []
    }
    for message in response["messages"]:

        message_content = {
            "created_by": message["user"]["name"],
            "body": message["body"],
            "created_at": message["created_at"],
            "mentioned_symbols": message["symbols"]
        }

        data["messages"].append(message_content)

    return data


def get_stocktwits_trending():
    request = requests.get("https://api.stocktwits.com/api/2/streams/trending.json")
    if request.status_code != 200:
        return {"error": "Invalid request, something went wrong"}

    response = request.json()
    trending = {}

    for message in response["messages"]:
        symbols = message["symbols"]
        for symbol in symbols:
            if symbol["symbol"] not in trending:
                trending[symbol["symbol"]] = symbol

    return trending


#print(get_stocktwits_trending())
#print(get_stocktwits_symbol_info('TSLA'))
