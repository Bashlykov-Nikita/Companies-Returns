# Companies-Returns
### Description: 
This project allows you to obtain historical data on the profits of companies included in some of the most popular indices:
- S&P 500 (United States)
- Nasdaq 100 (United States)
- CAC 40 (France)
- FTSE 100 (United Kingdom)
- DAX (Germany)
- HSI (Hong Kong (China))
- Nikkei 225 (Japan)

### Features: 
- Creates tabular files from historical returns data of companies:

  _d - files with daily returns
  
  _m - files with monthly returns.
- Updates .csv files every month using GitHub Actions.

### To Fetch the .csv files use:
```sh
url = "https://github.com/Bashlykov-Nikita/Companies-Returns/blob/main/${file_name}.csv?raw=true"
```
### Example:
```python
import pandas as pd
test_url = "https://github.com/Bashlykov-Nikita/Companies-Returns/blob/main/DowJones_d.csv?raw=true"
df = pd.read_csv(test_url, index_col=0)
```
