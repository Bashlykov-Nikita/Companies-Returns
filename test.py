import numpy as np
import pandas as pd
import yfinance as yf

pd.set_option("mode.use_inf_as_na", True)
### Indexes: S&P 500, Nasdaq Composite, Dow Jones Industrial Average,
#          Russell 2000, FTSE 100, DAX PERFORMANCE-INDEX, CAC 40,
#          Nikkei 225, HANG SENG INDEX.

# Indexes shot names:

index_names = [
    ("^GSPC", "SP500"),
    ("^IXIC", "NasdaqComposite"),
    ("^DJI", "DowJones"),
    ("^FTSE", "FTSE100"),
    ("^GDAXI", "DAX"),
    ("^HSI", "HSI"),
    ### Not added yet:
    ("^RUT", "Russell2000"),
    ("^FCHI", "CAC40"),
    ("^N225", "Nikkei225"),
]


###* Components URLs for: S&P 500, Nasdaq Composite, Dow Jones Industrial Average,
# *                      FTSE 100, DAX PERFORMANCE-INDEX, HANG SENG INDEX.
components_urls = {
    "SP500": "https://yfiua.github.io/index-constituents/constituents-sp500.csv",
    "NasdaqComposite": "https://yfiua.github.io/index-constituents/constituents-nasdaq100.csv",
    "DowJones": "https://yfiua.github.io/index-constituents/constituents-dowjones.csv",
    "FTSE100": "https://yfiua.github.io/index-constituents/constituents-ftse100.csv",
    "DAX": "https://yfiua.github.io/index-constituents/constituents-dax.csv",
    "HSI": "https://yfiua.github.io/index-constituents/constituents-hsi.csv",
}


def get_components(url):
    """
    Returns companies names from url.
    """
    if url:
        return pd.read_csv(url)["Symbol"]
    else:
        return "Components data is not available yet :("


def companies_returns_df(companies):
    """
        Calculate daily returns for a list of companies.
    Args:
        companies (pd.Series): names of companies

    Returns:
        pd.DataFrame: DataFrame of all companies returns starting from 1990 (if possible)
    """
    tickers = companies
    first_ticker_data = yf.download(companies[0], start="1990-01-01")
    # Create an empty DataFrame
    companies_df = pd.DataFrame(index=first_ticker_data.index, columns=tickers)

    # Fetch historical data for each ticker and populate the DataFrame
    for ticker in tickers:
        try:
            data = yf.download(ticker, start="1990-01-01")
            if data.empty:
                companies_df[ticker] = np.nan
            else:
                # Daily return:
                data["Return"] = (data["Close"] - data["Open"]) / data["Open"]
                companies_df[ticker] = data["Return"]
        except Exception as e:
            print(f"Error fetching data for {ticker}: {e}")
            companies_df[ticker] = (
                None  # Or handle the error differently, e.g., fill with 0
            )
    return companies_df


###* Daily components returns for each index:
sp500 = companies_returns_df(get_components(components_urls["SP500"]))
nasdaq100 = companies_returns_df(get_components(components_urls["NasdaqComposite"]))
dowjones = companies_returns_df(get_components(components_urls["DowJones"]))
ftse100 = companies_returns_df(get_components(components_urls["FTSE100"]))
dax = companies_returns_df(get_components(components_urls["DAX"]))
hsi = companies_returns_df(get_components(components_urls["HSI"]))

### Array to iterate
index_components_histoical_data = [sp500, nasdaq100, dowjones, ftse100, dax, hsi]


def clean_data(daily_hist_data):
    """
    Clean the daily historical data by removing any companies with not enough data.

    Args:
        daily_hist_data (list[pd.DataFrame]): List of companies historical returns for each index.

    Returns:
        list[pd.DataFrame]: A list of cleaned DataFrames with no missing values.
    """
    cleaned_data = []
    for index_data in daily_hist_data:
        buff = index_data.copy()
        buff = buff.dropna(axis=1)
        cleaned_data.append(buff)
    return cleaned_data


### Array to iterate
cleaned_data = clean_data(index_components_histoical_data)


def compound(r):
    """
    returns the result of compounding the set of returns in r
    """
    return np.expm1(np.log1p(r).sum())


### Converting daily data to monthly:
def to_period_m(cleaned_data):
    """
    Converts daily returns to monthly.
    """
    cleaned_data_m = []
    for index_data in cleaned_data:
        buff = index_data.copy()
        buff = buff.resample("M").apply(compound).to_period("M")
        cleaned_data_m.append(buff)
    return cleaned_data_m


### Converting clean companies returns data into csv files:
def convert_to_csv(cleaned_data, monthly=False):
    """
    Creates CSV files for daily/monthly returns data.
    """
    i = 0
    if monthly:
        for index_data in cleaned_data:
            index_data.to_csv(f"{index_names[i][1]}_m.csv", index=True)
            i = i + 1
    else:
        for index_data in cleaned_data:
            index_data.to_csv(f"{index_names[i][1]}_d.csv", index=True)
            i = i + 1