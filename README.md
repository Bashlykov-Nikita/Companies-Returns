# Companies-Returns
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
