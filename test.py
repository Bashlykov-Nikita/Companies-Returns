import requests
from bs4 import BeautifulSoup


def get_components_names(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "lxml")

    # Find the HTML elements containing the component names (adjust the selector as needed)
    components = soup.find_all(
        "a", class_="apply-common-tooltip tickerNameBox-GrtoTeat tickerName-GrtoTeat"
    )
    # Extract the component names from the elements
    component_names = [component.text for component in components]
    return component_names


len(get_components_names("https://www.tradingview.com/symbols/SPX/components/"))


### Indexes: S&P 500, Nasdaq Composite, Dow Jones Industrial Average,
#          Russell 2000, FTSE 100, DAX PERFORMANCE-INDEX, CAC 40,
#          Nikkei 225, HANG SENG INDEX.
# * Less then 100 components:
nas100_url = "https://www.tradingview.com/symbols/NASDAQ-NDX/components/"
dowjones_url = "https://www.tradingview.com/symbols/TVC-DJI/components/"
ftse100_url = "https://www.tradingview.com/symbols/TVC-UKX/components/"
DAX_url = "https://www.tradingview.com/symbols/XETR-DAX/components/"
cac40_url = "https://www.tradingview.com/symbols/EURONEXT-PX1/components/"
