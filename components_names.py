import requests
from bs4 import BeautifulSoup
import pandas as pd
import urls


def components_sp500(url: str) -> pd.Series:
    return pd.read_html(url)[0]["Symbol"]


def soup(url: str):
    response = requests.get(url)
    return BeautifulSoup(response.content, "lxml")


def components_TV(url: str) -> pd.Series:
    components = soup(url).find_all(
        "a", class_="apply-common-tooltip tickerNameBox-GrtoTeat tickerName-GrtoTeat"
    )
    component_names = pd.Series([component.text for component in components])
    return component_names


def components_nikkei(url: str) -> pd.Series:
    components = soup(url).find_all("td")
    components_names = []
    for td in components:
        text = td.text.strip()
        try:
            int(text)  # Check if the text can be converted to an int
            components_names.append(text + ".T")
        except ValueError:
            pass
        # component_names = [table.td.text + ".T" for table in component]
    return pd.Series(components_names)


def get_components_from_csv(url: str) -> pd.Series:
    """Returns companies names from csv url.

    Args:
        url (str): Url to a csv file

    Returns:
        pd.Series: Series of companies names
    """
    try:
        return pd.read_csv(url)["Symbol"]
    except Exception as e:
        print(f"Error reading CSV file from {url}: {e}")
        return pd.Series()


try:
    sp500 = components_sp500(urls.sp500_from_wiki["SP500"])
except Exception as e:
    print(f"Was not able to fetch: {e}")
    print("Trying diffrent sourse")
    sp500 = get_components_from_csv(urls.components_urls["SP500"])


# * Test
components_nikkei(urls.nikkei_from_nikkei["Nikkei225"])
