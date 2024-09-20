### Indexes: S&P 500, Nasdaq Composite, Dow Jones Industrial Average,
#          FTSE 100, DAX PERFORMANCE-INDEX, CAC 40,
#          Nikkei 225, HANG SENG INDEX.

sp500_from_wiki = {"SP500": "https://en.wikipedia.org/wiki/List_of_S%26P_500_companies"}

components_from_TradingView = {
    "Nasdaq100": "https://www.tradingview.com/symbols/NASDAQ-NDX/components/",
    "DowJones": "https://www.tradingview.com/symbols/TVC-DJI/components/",
    "FTSE100": "https://www.tradingview.com/symbols/TVC-UKX/components/",
    "DAX": "https://www.tradingview.com/symbols/XETR-DAX/components/",
    "CAC40": "https://www.tradingview.com/symbols/EURONEXT-PX1/components/",
    # ? With modifications .HK
    "HSI": "https://www.tradingview.com/symbols/HSI-HSI/components/",
}

nikkei_from_nikkei = {
    # ? Nikkei225 with modification .T
    "Nikkei225": "https://indexes.nikkei.co.jp/en/nkave/index/component"
}

### Alternative omponents URLs to csv files for: S&P 500, Nasdaq 100, Dow Jones Industrial Average,
#                       FTSE 100, DAX PERFORMANCE-INDEX, HANG SENG INDEX.
components_urls = {
    "SP500": "https://yfiua.github.io/index-constituents/constituents-sp500.csv",
    "Nasdaq100": "https://yfiua.github.io/index-constituents/constituents-nasdaq100.csv",
    "DowJones": "https://yfiua.github.io/index-constituents/constituents-dowjones.csv",
    "FTSE100": "https://yfiua.github.io/index-constituents/constituents-ftse100.csv",
    "DAX": "https://yfiua.github.io/index-constituents/constituents-dax.csv",
    "HSI": "https://yfiua.github.io/index-constituents/constituents-hsi.csv",
}
