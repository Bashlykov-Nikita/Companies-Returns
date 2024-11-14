# Get Historical Index Profits with Python! 🚀
### Description: 
This project allows you to obtain historical data on the profits of companies included in some of the most popular indices:
- S&P 500 🇺🇸
- Nasdaq 100 🇺🇸
- Dow Jones Industrial Average 🇺🇸
- CAC 40 🇫🇷
- FTSE 100 🇬🇧
- DAX 🇩🇪
- HSI 🇭🇰
- Nikkei 225 🇯🇵

### What it does:
- Creates tabular files from historical returns data of companies:  
  ```_d``` - files with daily returns📅   
  ```_m``` - files with monthly returns📈
- Updates ```.csv``` files every month using GitHub Actions.
### How it works:

1) ```urls.py``` - contains URLs of websites that include the names of components (companies) in the indices🔗.
2) ```components_names.py``` - extracts component names from these websites using Beautiful Soup🔍.
3) ```main.py``` - fetches historical data from yfinance using the extracted component names📊 &#8594; calculates daily and monthly profits💰 &#8594; creates a DataFrame for all companies in the index📄 &#8594; generates .csv files from these DataFrames💾.



### How to use:
To Fetch the .csv files use:
```sh
url = "https://github.com/Bashlykov-Nikita/Companies-Returns/blob/main/data/${file_name}.csv?raw=true"
```
### Example:
```python
import pandas as pd
test_url = "https://github.com/Bashlykov-Nikita/Companies-Returns/blob/main/data/DowJones_d.csv?raw=true"
df = pd.read_csv(test_url, index_col=0)
```
### Next Step!
Want to see how this data can be used to create investment portfolios?  
Check out my next project [Creating-Portfolios](https://github.com/Bashlykov-Nikita/Creating-Portfolio) where I'll be leveraging this data to build and analyze various portfolio strategies.

### Data Sources:
* [Wiki](https://en.wikipedia.org/wiki/List_of_S%26P_500_companies)
* [TradingView](www.tradingview.com)
* [Nikkei225](https://indexes.nikkei.co.jp/en/nkave/index/component)
* [yfiua](https://github.com/yfiua/index-constituents/tree/main?tab=readme-ov-file)

### Author:
[Nikita Bashlykov](https://github.com/Bashlykov-Nikita)

