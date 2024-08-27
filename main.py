import numpy as np
import pandas as pd
import yfinance as yf

# Indexes: S&P 500, Nasdaq Composite, Dow Jones Industrial Average,
#          Russell 2000, FTSE 100, DAX PERFORMANCE-INDEX, CAC 40,
#          Nikkei 225, HANG SENG INDEX.
# Indexes shot names:

index_names = [
    "^GSPC",
    "^IXIC",
    "^DJI",
    "^RUT",
    "^FTSE",
    "^GDAXI",
    "^FCHI",
    "^N225",
    "^HSI",
]


# Components URLs for: S&P 500, Nasdaq Composite, Dow Jones Industrial Average,
#                      FTSE 100, DAX PERFORMANCE-INDEX, HANG SENG INDEX.
components_urls = [
    "https://yfiua.github.io/index-constituents/constituents-sp500.csv",
    "https://yfiua.github.io/index-constituents/constituents-nasdaq100.csv",
    "https://yfiua.github.io/index-constituents/constituents-dowjones.csv",
    "https://yfiua.github.io/index-constituents/constituents-ftse100.csv",
    "https://yfiua.github.io/index-constituents/constituents-dax.csv",
    "https://yfiua.github.io/index-constituents/constituents-hsi.csv",
]


def get_components(url):
    if url:
        return pd.read_csv(url)["Symbol"]
    else:
        return "Components data is not available yet :("


def companies_returns_df(companies):
    tickers = companies
    first_ticker_data = yf.download(companies[0], period="max")
    # Create an empty DataFrame
    companies_df = pd.DataFrame(index=first_ticker_data.index, columns=tickers)

    # Fetch historical data for each ticker and populate the DataFrame
    for ticker in tickers:
        try:
            data = yf.download(ticker, period="max")
            if data.empty:
                companies_df[ticker] = 0
            else:
                # data["Return"] = data["Close"].pct_change()
                data["Return"] = (data["Close"] - data["Open"]) / data["Open"]
                companies_df[ticker] = data["Return"]
        except Exception as e:
            print(f"Error fetching data for {ticker}: {e}")
            companies_df[ticker] = (
                None  # Or handle the error differently, e.g., fill with 0
            )
    return companies_df


# Daily components returns for each index:
sp500 = companies_returns_df(get_components(components_urls[0]))
nasdaq100 = companies_returns_df(get_components(components_urls[1]))
dowjones = companies_returns_df(get_components(components_urls[2]))
ftse100 = companies_returns_df(get_components(components_urls[3]))
dax = companies_returns_df(get_components(components_urls[4]))
hsi = companies_returns_df(get_components(components_urls[5]))

# Array to iterate
index_components_histoical_data = [sp500, nasdaq100, dowjones, ftse100, dax, hsi]

test = sp500.dropna(axis="columns", how="all")
test = test.dropna()

# def clean_data(daily_hist_data):
