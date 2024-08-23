import numpy as np
import pandas as pd
import yfinance as yf

index_name = "^GSPC"
components_url = "https://yfiua.github.io/index-constituents/constituents-sp500.csv"


def companies_returns_df(companies):
    tickers = companies
    first_ticker_data = yf.download(companies[0], period="max")
    # Create an empty DataFrame with a single row
    companies_df = pd.DataFrame(index=first_ticker_data.index, columns=tickers)

    # Fetch historical data for each ticker and populate the DataFrame
    for ticker in tickers:
        try:
            data = yf.download(ticker, period="max")
            if data.empty:
                companies_df[ticker] = 0
            else:
                data["Return"] = (data["Close"] - data["Open"]) / data["Open"]
                companies_df[ticker] = data["Return"]
        except Exception as e:
            print(f"Error fetching data for {ticker}: {e}")
            companies_df[ticker] = (
                None  # Or handle the error differently, e.g., fill with 0
            )
    return companies_df
