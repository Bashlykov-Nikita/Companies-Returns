import numpy as np
import pandas as pd
import yfinance as yf
import components_names as cn
import urls

pd.set_option("mode.use_inf_as_na", True)

indexes_components = {
    **cn.get_components(urls.sp500_from_wiki, cn.components_sp500),
    **cn.get_components(urls.components_from_TradingView, cn.components_TV),
    **cn.get_components(urls.nikkei_from_nikkei, cn.components_nikkei),
}
indexes_components["HSI"]


def companies_returns_df(companies: pd.Series) -> pd.DataFrame:
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


def returns_dict(indexes_components: dict) -> dict:
    """
    Calculate historical data and returns for a dictionary of indexes.

    Args:
        indexes_components (dict): Dictionary containing index components names

    Returns:
        dict: Dictionary with historical returns data for each index
    """
    index_components_histoical_data = {}
    for key in indexes_components:
        print(f"Downloading historical data and calculating returns for {key}")
        index_components_histoical_data[key] = companies_returns_df(
            indexes_components[key]
        )

    return index_components_histoical_data


### Array to iterate
index_components_histoical_data = returns_dict(indexes_components)


def clean_data(daily_hist_data: list[pd.DataFrame]) -> list[pd.DataFrame]:
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
cleaned_data = clean_data(index_components_histoical_data.values())


def compound(r):
    """
    returns the result of compounding the set of returns in r
    """
    return np.expm1(np.log1p(r).sum())


### Converting daily data to monthly:
def to_period_m(cleaned_data: list[pd.DataFrame]) -> list[pd.DataFrame]:
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
def convert_to_csv(cleaned_data: list[pd.DataFrame], monthly=False):
    """
    Converts cleaned data to CSV files either daily or monthly.
    Args:
        cleaned_data (List[pd.DataFrame]): The cleaned data to be converted to CSV.
        monthly (bool, optional): Flag to indicate whether to save data monthly. Defaults to False.
    """
    if monthly:
        for index_data, key in zip(cleaned_data, indexes_components.keys()):
            index_data.to_csv(f"{key}_m.csv", index=True)
            print(f"{key}_m.csv")
    else:
        for index_data, key in zip(cleaned_data, indexes_components.keys()):
            index_data.to_csv(f"{key}_d.csv", index=True)
            print(f"{key}_d.csv")


### Creating CSV files for daily and monthly companies returns:

convert_to_csv(cleaned_data)
convert_to_csv(to_period_m(cleaned_data), monthly=True)


pd.read_csv("FTSE100_m.csv", index_col=0)
