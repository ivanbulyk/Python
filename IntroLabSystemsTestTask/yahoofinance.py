# you'll need to install all dependencies: yfinance, pandas etc.

import yfinance as yf
from bs4 import BeautifulSoup
import urllib.request
import pandas as pd

symbol = input("Enter stock symbol please: ")

# ------------------------------------------
symbol_data = yf.Ticker(symbol.upper())

# get stock info
print(symbol_data.info)

# get historical market data
hist = symbol_data.history(period="max")
print(hist)

# Download stock data then export as CSV
data_df = yf.download(symbol.upper(), period="max")
data_df.to_csv(f'{symbol.lower()}.csv')

df = pd.read_csv(f"{symbol.lower()}.csv")

# Initialize an empty list
_3day_before_change = []

for i in range(len(df["Close"]) - 1, -1, -1):
    if i >= 3:
        value = df["Close"][i] / df["Close"][i - 3]
        _3day_before_change.append(value)

    else:
        value = "No matching the condition"
        _3day_before_change.append(value)

_3day_before_change.reverse()
df["_3day_before_change"] = _3day_before_change
print(df)

df.to_csv(f'{symbol.lower()}.csv', index=False)
# ------------------------------------------
# ------------------------------------------
url = f"https://finance.yahoo.com/quote/{symbol.upper()}/news"

headers = {
    'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 '
                  'Safari/537.3'}
# download the URL and extract the content to the variable html
request = urllib.request.Request(url, headers=headers)
html = urllib.request.urlopen(request).read()

# pass the HTML to Beautifulsoup.
soup = BeautifulSoup(html, 'html.parser')

# get the HTML of the table called site Table where all the links are displayed
main_table = soup.find("div", attrs={'id': 'latestQuoteNewsStream-0-Stream'})

links = main_table.find_all("a")
# from each link extract the text of link and the link itself
# Lists to store the data we extracted
news_urls = []
news_titles = []
yahoo_news_url = "https://finance.yahoo.com"

for link in links:
    title = link.text
    url = link['href']

    # Check if a URL is absolute
    if not url.startswith('http'):
        url = yahoo_news_url + url
        if yahoo_news_url in url:
            news_urls.append(url)
            news_titles.append(title)
            print("%s - %s" % (title, url))

df = pd.DataFrame({'Link': news_urls, 'Title': news_titles})

df.to_csv(f'{symbol.lower()}_news.csv', index=False)