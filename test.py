import requests
from bs4 import BeautifulSoup

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
    #! With modifications .HK
    "HSI": "https://www.tradingview.com/symbols/HSI-HSI/components/",
}

nikkei_from_nikkei = {
    #! Nikkei225 with modification .T
    "Nikkei225": "https://indexes.nikkei.co.jp/en/nkave/index/component"
}


def TV_mod(soup):
    return soup.find_all(
        "a", class_="apply-common-tooltip tickerNameBox-GrtoTeat tickerName-GrtoTeat"
    )


def wiki_mod(soup):
    return soup.find_all("a", class_="external text")


def get_components_names(url: str, mod=wiki_mod):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "lxml")

    # Find the HTML elements containing the component names (adjust the selector as needed)
    components = mod(soup)
    # Extract the component names from the elements
    component_names = [component.text for component in components]
    return component_names


get_components_names(sp500_from_wiki["SP500"])


tickers = pd.read_html("https://en.wikipedia.org/wiki/List_of_S%26P_500_companies")[0][
    "Symbol"
]
