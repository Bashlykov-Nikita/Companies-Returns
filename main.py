import numpy as np
import pandas as pd
import yfinance as yf

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


### Components URLs for: S&P 500, Nasdaq Composite, Dow Jones Industrial Average,
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
                # data["Return"] = data["Close"].pct_change()
                data["Return"] = (data["Close"] - data["Open"]) / data["Open"]
                companies_df[ticker] = data["Return"]
        except Exception as e:
            print(f"Error fetching data for {ticker}: {e}")
            companies_df[ticker] = (
                None  # Or handle the error differently, e.g., fill with 0
            )
    return companies_df


### Daily components returns for each index:
sp500 = companies_returns_df(get_components(components_urls[0]))
nasdaq100 = companies_returns_df(get_components(components_urls[1]))
dowjones = companies_returns_df(get_components(components_urls[2]))
# TODO: change indexing
ftse100 = companies_returns_df(get_components(components_urls[3]))
dax = companies_returns_df(get_components(components_urls[4]))
hsi = companies_returns_df(get_components(components_urls[5]))

# Array to iterate
index_components_histoical_data = [sp500, nasdaq100, dowjones, ftse100, dax, hsi]

pd.set_option("mode.use_inf_as_na", True)


def clean_data(daily_hist_data):
    cleaned_data = []
    for index_data in daily_hist_data:
        buff = index_data.copy()
        buff = buff.dropna(axis=1)
        cleaned_data.append(buff)
    return cleaned_data


cleaned_data = clean_data(index_components_histoical_data)
cleaned_data[5]


### Converting clean companies returns data into csv files:
def convert_to_csv(clean_data, monthly=False):
    i = 0
    if monthly:
        for index_data in clean_data:
            index_data.to_csv(f"{index_names[i][1]}_m.csv", index=False)
            i = i + 1
    else:
        for index_data in clean_data:
            index_data.to_csv(f"{index_names[i][1]}_d.csv", index=False)
            i = i + 1


# FIXME: Problem with double indexing
convert_to_csv(cleaned_data)


### Testing

test = get_components(components_urls[3])
test1 = yf.download(test[0], start="1990-01-01")

print(f"{index_names[1][1]}")
df = pd.read_csv("SP500_d.csv")
df1 = pd.read_csv("FTSE100_d.csv")

df.index
df1.index
