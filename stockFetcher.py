from polygon import RESTClient

client = RESTClient("mDLfNuVMyN6gAuuTpY6JWyNs9ceZKBx8")

aggs = []
closing_prices= []
for a in client.list_aggs(
    "AAPL",
    1,
    "minute",
    "2023-01-09",
    "2023-02-10",
    adjusted="true",
    sort="asc",
    limit=120,
):
    aggs.append(a)
    closing_prices.append(a.close)

print(closing_prices)
