import requests
from bs4 import BeautifulSoup
import pandas as pd
import urls


def components_sp500(url: str) -> pd.Series:
    """Retrieve the S&P 500 symbols from the specified URL.

    Args:
        url (str): The URL to fetch the data from.

    Returns:
        pd.Series: A pandas Series containing the symbols.
    """
    return pd.read_html(url)[0]["Symbol"]


def soup(url: str):
    """Send a GET request to the specified URL and return the parsed content
    using BeautifulSoup.

    Args:
        url (str): The URL to send the GET request to.

    Returns:
        BeautifulSoup: Parsed content of the response using the 'lxml' parser.
    """
    response = requests.get(url)
    return BeautifulSoup(response.content, "lxml")


def components_TV(url: str) -> pd.Series:
    """Retrieve the names of components from the specified URL using BeautifulSoup.

    Args:
        url (str): The URL to extract component names from.

    Returns:
        pd.Series: A pandas Series containing the names of the components.
    """
    components = soup(url).find_all(
        "a", class_="apply-common-tooltip tickerNameBox-GrtoTeat tickerName-GrtoTeat"
    )
    if "HSI-HSI" in url:
        component_names = pd.Series(
            [component.text.zfill(4) + ".HK" for component in components]
        )
    else:
        component_names = pd.Series([component.text for component in components])

    return component_names


def components_nikkei(url: str) -> pd.Series:
    """
    Retrieve Nikkei components names from the provided URL.

    Args:
        url (str): The URL to fetch the components names from.

    Returns:
        pd.Series: A pandas Series containing the Nikkei components names.
    """
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


def get_components(indexes: dict, function) -> dict:
    """Retrieves components for each index from the sources.

    Args:
        indexes (dict): Dictionary containing index names as keys
            and corresponding source URLs as values.
        function (function): Function to retrieve components from a source URL.

    Returns:
        dict: Dictionary with index names as keys and retrieved components as values.
    """
    index_dict = {}
    for key in indexes:
        try:
            print("Getting components from main source")
            components = function(indexes[key])
            index_dict[key] = components
        except Exception as e:
            print(f"Was not able to fetch: {e}")
            print("Trying diffrent source")
            if key in urls.components_urls.keys():
                components = get_components_from_csv(urls.components_urls[key])
                index_dict[key] = components
            else:
                print("No sources available :(")
    return index_dict
