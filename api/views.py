import re
import json
import requests
from bs4 import BeautifulSoup
from urllib.request import Request, urlopen


def get_html(url):
    # helper function that returns html of url
    req = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    webpage = urlopen(req).read()
    html = BeautifulSoup(webpage, "html.parser")
    return html


def get_market_data(name):
    # Takes in the name (shortened) of the stock and returns most useful data in a dictionary
    # Set up scraper
    url = "https://ca.finance.yahoo.com/quote/" + name
    html = get_html(url)

    pattern = re.compile(r'\s--\sData\s--\s')
    script_data = html.find('script', text=pattern).contents[0]
    # find the starting position of the json string
    start = script_data.find("context") - 2

    # slice the json string
    try:
        json_data = json.loads(script_data[start:-12])
        price_data = json_data["context"]["dispatcher"]["stores"]["QuoteSummaryStore"]["price"]
        summary = json_data["context"]["dispatcher"]["stores"]["QuoteSummaryStore"]["summaryDetail"]
    except:
        print("NAME ERROR 1 ", name)
        return {"error": f"Invalid stock name of {name}"}

    # useful data
    all_stock_data = {}
    keys = ["volume", "open", "close", "high", "low", "marketCap", "PERatio", "dividendYield", "annualHigh", "annualLow"]
    values = ["regularMarketVolume", "regularMarketOpen", "regularMarketPreviousClose", "regularMarketDayHigh", "regularMarketDayLow", "marketCap", "trailingPE", "dividendYield", "fiftyTwoWeekHigh", "fiftyTwoWeekLow"]
    all_stock_data["name"] = price_data["shortName"]

    for x in range(len(keys)):
        if x < 6:
            data = price_data
        else:
            data = summary
        if data.get(values[x]) and data[values[x]].get("raw"):
            all_stock_data[keys[x]] = data[values[x]]["raw"]
        else:
            all_stock_data[keys[x]] = "N/A"
    return all_stock_data


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

def get_reddit_trending(num):
    request = requests.get("https://apewisdom.io/api/v1.0/filter/all-stocks/page/1")
    response = request.json()
    trending = {}
    for i in range(num):
        trending[response["results"][i]["ticker"]] = [response["results"][i]["mentions"], response["results"][i]["upvotes"]]
    
    return trending

#print(get_market_data("tsla"))