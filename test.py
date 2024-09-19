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


def soup(url: str):
    response = requests.get(url)
    return BeautifulSoup(response.content, "lxml")


def components_TV(url: str):
    components = soup(url).find_all(
        "a", class_="apply-common-tooltip tickerNameBox-GrtoTeat tickerName-GrtoTeat"
    )
    component_names = [component.text for component in components]
    return component_names


def components_nikkei(url: str):
    components = soup(url).find_all("td")
    components_names = []
    for td in components:
        text = td.text.strip()
        try:
            int(text)  # Check if the text can be converted to a float
            components_names.append(text + ".T")
        except ValueError:
            pass
        # component_names = [table.td.text + ".T" for table in component]
    return components_names


len(components_nikkei(nikkei_from_nikkei["Nikkei225"]))

components_TV(components_from_TradingView["Nasdaq100"])[0]


tickers = pd.read_html("https://indexes.nikkei.co.jp/en/nkave/index/component")[0][
    "Code"
]
