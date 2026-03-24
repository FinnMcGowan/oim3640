import yfinance as yf
# Yahoo! Finance API
'''
stock = yf.Ticker("AAPL")
info = stock.info
print(info['shortName'])
print(info['currentPrice'])

tickers = ['AAPL', 'NVDA', 'MSFT']
prices = {}
for t in tickers:

print(prices)

print(sorted(prices)) # create a new list of the keys in prices, sorted alphabetically
print(sorted(prices.values()))

print(tickers)


# how to sort stocks by values, but still to show k: v ?

prices = {'AAPL: [252.53, `300]', 'NVDA: [195.55, 250]', 'MSFT: [280.00, 350]'}

print(sum(prices.values()))

total = 0
for price in prices.values():
    total += price[1]
    print(total)


'''
# BUILDING DICTIONARIES
tickers = ['AAPL', 'NVDA', 'MSFT', 'META', 
'GOOG']
stocks = {} # {'NVDA': [open, currentPrice, volume]}


for t in tickers: 
    # Creates List (square bracket)
    stocks[t] = [yf.Ticker(t).info['open'], yf.Ticker(t).info['currentPrice'], yf.Ticker(t).info['volume']]

    # Creates a Tuple (parentheses)
    #stocks[t] = yf.Ticker(t).info['open'], yf.Ticker(t).info['currentPrice'], yf.Ticker(t).info['volume']

    info_list = {}
    for name in ['open', 'currentPrice', 'volume']:
        info_list[name] = yf.Ticker(t).info[name]
    stocks[t] = info_list


print(stocks)

# change list to dictionary (add keys to list)

# NEW DATA STRUCTURE: 'set'
