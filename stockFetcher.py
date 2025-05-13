from polygon import RESTClient
import matplotlib.pyplot as plt
from mplfinance.original_flavor import candlestick_ohlc
import pandas as pd
import matplotlib.dates as mpldates
import numpy as np

client = RESTClient("mDLfNuVMyN6gAuuTpY6JWyNs9ceZKBx8")

aggs = []
close_prices= []
open_prices = []
high_prices = []
low_prices = []
indices = []
for a in client.list_aggs(
    "AAPL",
    1,
    "minute",
    "1747060200", #unix timestamp
	"1747083600",
    adjusted="true",
    sort="asc",
    limit=120,
):
	aggs.append(a)
	close_prices.append(a.close)
	open_prices.append(a.open)
	high_prices.append(a.high)
	low_prices.append(a.low)

indices = list(range(len(aggs)))

stock_prices = pd.DataFrame({'index': indices,
                             'open': open_prices,
                             'close': close_prices,
                             'high': high_prices,
                             'low': low_prices})

ohlc = stock_prices.loc[:, ['index', 'open', 'high', 'low', 'close']]
ohlc = ohlc.astype(float)

# Creating Subplots
fig, ax = plt.subplots()

candlestick_ohlc(ax, ohlc.values, width=0.6, colorup='green',
                 colordown='red', alpha=0.4)

# Setting labels & titles
ax.set_xlabel('Index')
ax.set_ylabel('Price')
fig.suptitle('Stock Prices of trading day')

# Formatting Date
fig.autofmt_xdate()

fig.tight_layout()

plt.show()