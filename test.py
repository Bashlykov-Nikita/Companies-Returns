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


url = "https://www.tradingview.com/symbols/SPX/components/"

# Send request and get the response
