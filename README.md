# NSETools

Python library for extracting data from National Stock Exchange (India)

## Table of Contents

- [Disclaimer](#disclaimer)
- [Installation](#installation)
- [Usage](#usage)
- [API Reference](#api-reference)
  - [Stock APIs](#stock-apis)
    - [Get Stock Codes](#1-get-stock-codes)
    - [Get Stock Quote](#2-get-stock-quote)
    - [Check Valid Stock Code](#3-check-valid-stock-code)
    - [52 Week High/Low](#4-52-week-highlow)
  - [Index APIs](#index-apis)
    - [Get Index Quote](#1-get-index-quote)
    - [Get Index List](#2-get-index-list)
    - [Get All Index Quotes](#3-get-all-index-quotes)
    - [Top Gainers & Losers](#4-top-gainers--losers)
    - [Advances & Declines](#5-advances--declines)
    - [Get Stocks in Index](#6-get-stocks-in-index)
    - [Get Stock Quotes in Index](#7-get-stock-quotes-in-index)
  - [Derivatives APIs](#derivatives-apis)
    - [Get Future Quote](#1-get-future-quote)
- [Response Formats](#response-formats)
- [Response Examples](#response-examples)
  - [Stock Quote Response](#stock-quote-response)
  - [Index Quote Response](#index-quote-response)
- [Setting up Dev Environment](#setting-up-dev-environment)
  - [Clone and Install](#clone-the-repo-and-install-dependencies)
  - [Running Tests](#running-tests)
  - [Make Utilities](#other-make-utilities)
- [License](#license)
- [Updates](#updates)

## DISCLAIMER

- This library is intended **only for educational and informational purposes**. It does not provide financial, trading, or investment advice. Users should verify data independently before making any financial decisions.  
- It **only retrieves publicly available data** from the official website without requiring authentication, login credentials, or bypassing any security measures. It does **not** scrape private, restricted, or real-time tick-by-tick data.  
- This project is **not affiliated with, endorsed by, or associated with the National Stock Exchange of India (NSE)** or any other financial institution. NSE retains all rights over its proprietary data, trademarks, and services.  
- Users are responsible for ensuring their use complies with applicable laws, regulations, and the terms of service of the data provider. The author assumes **no liability for any misuse or consequences** arising from the use of this tool.  
- This software is provided **"as is"**, without any warranties, express or implied. The author is **not liable** for any errors, inaccuracies, disruptions, or losses resulting from its use.  

[Back to Top](#nsetools)

## Installation

```bash
pip install nsetools
```

Currently prefer cloning the repo because, pip installable version is lagging the documentation and features. Update the PYTHONPATH to point to src directory.

[Back to Top](#nsetools)

## Usage

```python
from nsetools import Nse
nse = Nse()
```

[Back to Top](#nsetools)

## API Reference

### Stock APIs

1. **Get Stock Codes**
   ```python
   nse.get_stock_codes()
   ```
   Gets a list of stock codes traded in NSE.

   **Returns:**
   - `list`: List of strings containing stock symbols traded on NSE

   **Example:**
   ```python
   >>> nse.get_stock_codes()
   ['20MICRONS', '3IINFOTECH', '3MINDIA', '3PLAND', '63MOONS']
   ```

2. **Get Stock Quote**
   ```python
   nse.get_quote(code, all_data=False)
   ```
   Gets quote data for a given stock from NSE.

   **Arguments:**
   - `code` (str): NSE stock symbol/code for which quote is to be fetched
   - `all_data` (bool, optional): If True returns complete quote data, if False returns only price info. Defaults to False.

   **Returns:**
   - `dict`: Dictionary containing quote data

   **Example:**
   ```python
   >>> nse.get_quote('abb')
   {
       'lastPrice': 5189.1,
       'change': 70.55,
       'pChange': 1.38,
       'previousClose': 5118.55,
       'open': 5160,
       'close': 5187.65,
       'vwap': 5162.91,
       'stockIndClosePrice': 0,  # Added missing field
       'lowerCP': 4606.7,
       'upperCP': 5630.4,
       'pPriceBand': 'No Band',
       'basePrice': 5118.55,
       'intraDayHighLow': {'min': 5101, 'max': 5218.45, 'value': 5189.1},
       'weekHighLow': {'min': 4890}
   }

   >>> nse.get_quote('abb', all_data=True)  # Returns additional market depth data
   {
       'priceInfo': { ... },
       'securityInfo': { ... },
       'marketDeptOrderBook': { ... },
       'tradingInfo': { ... },
       'industryInfo': { ... }
   }
   ```

3. **Check Valid Stock Code**
   ```python
   nse.is_valid_code(code)
   ```
   Validates whether the provided stock code exists in the list of valid stock codes from NSE.

   **Arguments:**
   - `code` (str): Stock code/symbol to validate

   **Returns:**
   - `bool`: True if code is valid, False otherwise

   **Example:**
   ```python
   >>> nse.is_valid_code("INFY")
   True
   ```

4. **52 Week High/Low**
   ```python
   nse.get_52_week_high()
   nse.get_52_week_low()
   ```
   Retrieves list of stocks that have hit their 52-week high/low prices on NSE.

   **Returns:**
   - `list[dict]`: List of dictionaries containing stock details

   **Example:**
   ```python
   >>> nse.get_52_week_high()
   [
       {
           'symbol': 'AVANTIFEED',
           'series': 'EQ',
           'companyName': 'Avanti Feeds Limited',
           'new52WHL': 899,
           'prev52WHL': 849.9,
           'prevHLDate': '13-Mar-2025',
           'ltp': 887,
           'prevClose': 842.55,
           'change': 44.45,
           'pChange': 5.28
       },
       {...}
   ]

   >>> nse.get_52_week_low()  # Similar structure as 52-week high
   ```

[Back to Top](#nsetools)

### Index APIs

1. **Get Index Quote**
   ```python
   nse.get_index_quote(index="NIFTY 50")
   ```
   Retrieves detailed quote information for a given index code from NSE.

   **Arguments:**
   - `index` (str): The index code/symbol (e.g., "NIFTY 50", "BANKNIFTY")

   **Returns:**
   - `dict`: Dictionary containing index quote details

   **Example:**
   ```python
   >>> nse.get_index_quote("NIFTY 50")
   {
       'key': 'BROAD MARKET INDICES',
       'index': 'NIFTY 50',
       'indexSymbol': 'NIFTY 50', 
       'last': 22508.75,
       'variation': 111.55,
       'percentChange': 0.5,
       'open': 22353.15,
       'high': 22577.0,
       'low': 22353.15,
       'previousClose': 22397.2,
       'yearHigh': 26277.35,
       'yearLow': 21281.45,
       'pe': 26.45,
       'pb': 4.01,
       'dy': 1.2,
       'advances': 35,
       'declines': 15,
       'unchanged': 0
   }
   ```

2. **Get Index List**
   ```python
   nse.get_index_list()
   ```
   Gets list of all NSE index symbols.

   **Returns:**
   - `list[str]`: List of index symbols (e.g., ['NIFTY 50', 'NIFTY BANK', ...])

   **Example:**
   ```python
   >>> nse.get_index_list()
   ['NIFTY 50', 'NIFTY NEXT 50', 'NIFTY 100', 'NIFTY 200', 
    'NIFTY MIDCAP 50', 'NIFTY BANK', 'NIFTY AUTO', 'NIFTY IT',
    'NIFTY FMCG', 'NIFTY PHARMA', ...]
   ```

3. **Get All Index Quotes**
   ```python
   nse.get_all_index_quote()
   ```
   Gets quotes for all indices in a single call.
   ```python
   >>> nse.get_all_index_quote()
   [
       {
           'key': 'BROAD MARKET INDICES',
           'index': 'NIFTY 50',
           'indexSymbol': 'NIFTY 50', 
           'last': 22508.75,
           'variation': 111.55,
           'percentChange': 0.5,
           # ... other fields
       },
       {
           'index': 'NIFTY BANK',
           'indexSymbol': 'NIFTY BANK',
           # ... other fields
       },
       # ... other indices
   ]
   ```

4. **Top Gainers & Losers**
   ```python
   nse.get_top_gainers(index="NIFTY")
   nse.get_top_losers(index="NIFTY")
   ```
   Gets real-time data for stocks with highest gains/losses.

   **Arguments:**
   - `index` (str, optional): Index name for filtering. Defaults to "NIFTY".
     Valid values:
     - "NIFTY" or "NIFTY 50"
     - "BANKNIFTY" or "NIFTY BANK"
     - "NIFTYNEXT50" or "NIFTY NEXT 50"
     - "SECGTR20" (Securities > ₹20)
     - "SECLWR20" (Securities < ₹20)
     - "FNO" (Futures & Options)
     - "ALL" (All Securities)

   **Returns:**
   - `list[dict]`: List of dictionaries

   **Example:**
   ```python
   >>> gainers = nse.get_top_gainers()
   >>> gainers[0]  # Sample gainer
   {
       'symbol': 'DRREDDY',
       'series': 'EQ',
       'openPrice': 1107.9,
       'highPrice': 1154.1,
       'lowPrice': 1101.5,
       'ltp': 1151.5,
       'previousPrice': 1107.95,
       'net_price': 43.55,
       'tradedQuantity': 2714559,
       'turnoverInLakhs': 31016.01,
       'lastCorpAnnouncement': 'Annual General Meeting',
       'lastCorpAnnouncementDate': '28-Jul-2024',
       'perChange': 3.93
   }

   >>> losers = nse.get_top_losers()  # Added losers example
   >>> losers[0]  # Sample loser
   {
       'symbol': 'TATAMOTORS',
       'series': 'EQ',
       'openPrice': 375.0,
       'highPrice': 375.0,
       'lowPrice': 365.2,
       'ltp': 367.8,
       'previousPrice': 374.35,
       'net_price': -6.55,
       'tradedQuantity': 3714559,
       'turnoverInLakhs': 41016.01,
       'perChange': -1.75
   }
   ```

5. **Advances & Declines**
   ```python
   nse.get_advances_declines(index='nifty 50')
   ```
   Gets number of advancing and declining stocks in an index.

   **Arguments:**
   - `index` (str, optional): Name of the index. Defaults to 'nifty 50'
     Valid values include 'NIFTY 50', 'NIFTY BANK', etc.

   **Returns:**
   - `dict`: Dictionary containing:
     - `advances`: Number of advancing stocks
     - `declines`: Number of declining stocks

   **Example:**
   ```python
   >>> nse.get_advances_declines("NIFTY BANK")
   {'advances': 7, 'declines': 4}
   ```

6. **Get Stocks in Index**
   ```python
   nse.get_stocks_in_index(index="NIFTY 50")
   ```
   Gets list of stock symbols that are constituents of a given index.

   **Arguments:**
   - `index` (str, optional): Name of the NSE index. Defaults to "NIFTY 50".

   **Returns:**
   - `list`: List of stock symbols that are part of the specified index

   **Example:**
   ```python
   >>> nse.get_stocks_in_index("NIFTY BANK")
   ['AUBANK', 'AXISBANK', 'BANDHANBNK', 'FEDERALBNK', 'HDFCBANK', 
    'ICICIBANK', 'IDFCFIRSTB', 'INDUSINDBK', 'KOTAKBANK', 'PNB', 
    'SBIN', 'YESBANK']
   ```

7. **Get Stock Quotes in Index**
   ```python
   nse.get_stock_quote_in_index(index="NIFTY 50", include_index=False)
   ```
   Gets detailed real-time quotes for all stocks in a given index.

   **Arguments:**
   - `index` (str, optional): The name of the index. Defaults to "NIFTY 50"
   - `include_index` (bool, optional): Whether to include index quote in results. Defaults to False

   **Returns:**
   - `list`: List of dictionaries containing quote data for each stock

   **Example:**
   ```python
   >>> quotes = nse.get_stock_quote_in_index("NIFTY BANK", include_index=True)
   >>> quotes[0]  # Index quote when include_index=True
   {
       'priority': 1,
       'symbol': 'NIFTY BANK',
       'identifier': 'NIFTYBANK',
       'open': 44821.3,
       'dayHigh': 45065.85,
       'dayLow': 44752.95,
       'lastPrice': 44991.95,
       'previousClose': 44745.95,
       'change': 246.0,
       'pChange': 0.55,
       'totalTradedVolume': 0,
       'totalTradedValue': 0.0,
       'lastUpdateTime': '23-Mar-2024 15:30:00',
       'yearHigh': 48636.65,
       'yearLow': 40563.65,
       'perChange365d': 9.8,
       'perChange30d': 0.62
   }

   >>> # Stock quote example (either with include_index=True or False)
   >>> quotes[1] if include_index else quotes[0]  # First stock quote
   {
       'priority': 0,
       'symbol': 'HDFCBANK',
       'identifier': 'HDFCBANKEQN',
       'series': 'EQ',
       'open': 1460.0,
       'dayHigh': 1469.8,
       'dayLow': 1451.2,
       'lastPrice': 1465.9,
       'previousClose': 1453.35,
       'change': 12.55,
       'pChange': 0.86,
       'totalTradedVolume': 5841960,
       'totalTradedValue': 8557023518.4,
       'lastUpdateTime': '23-Mar-2024 15:30:00',
       'yearHigh': 1757.8,
       'yearLow': 1427.05
   }
   ```

[Back to Top](#nsetools)

### Derivatives APIs

1. **Get Future Quote**
   ```python
   nse.get_future_quote(code, expiry_date=None)
   ```
   Gets futures trading data for a stock.
   - `code`: Stock code for futures data
   - `expiry_date`: Optional expiry date (format: 'DD-Mon-YYYY')
   - Returns data for all expiries if expiry_date is None
   ```python
   >>> nse.get_future_quote('RELIANCE')
   [{
       'expiryDate': '27-Mar-2025',
       'lastPrice': 1246,
       'premium': 4.45,
       'openPrice': 1245.25,
       'highPrice': 1260.85,
       'lowPrice': 1236.2,
       'closePrice': 1247.9,
       'prevClose': 1244.8,
       'change': 1.2,
       'pChange': 0.10,
       'numberOfContractsTraded': 257812,
       'totalTurnover': 3214.56,
       'openInterest': 257812,
       'changeInOpenInterest': 7144,
       'pchangeinOpenInterest': 2.85,
       'marketLot': 500,
       'dailyVolatility': 14.2,
       'annualisedVolatility': 22.4
   }]

   >>> # With specific expiry date
   >>> nse.get_future_quote('RELIANCE', expiry_date='27-Mar-2025')
   {  # Returns single dictionary instead of list
      'expiryDate': '27-Mar-2025',
      # ... same fields as above
   }
   ```

[Back to Top](#nsetools)

## Response Formats

All APIs return either Python dictionaries or lists containing the requested data. Numeric values are automatically converted to appropriate Python types (int/float).

[Back to Top](#nsetools)

## Response Examples

### Stock Quote Response
```python
{
    'priceInfo': {
        'lastPrice': 2500.0,
        'change': 50.0,
        'pChange': 2.04,
        'open': 2460.0,
        'high': 2520.0,
        'low': 2455.0,
        'close': 2450.0,
        # ... additional fields when all_data=True
    }
}
```

### Index Quote Response
```python
{
    'indexSymbol': 'NIFTY 50',
    'lastPrice': 19500.0,
    'change': 100.0,
    'pChange': 0.52,
    'advances': 35,
    'declines': 15,
    # ... other fields
}
```

[Back to Top](#nsetools)

## Setting up Dev Environment

### Clone the repo and install dependencies

```bash
python -m venv nsetools-dev # skip this if you already have a virtual environment
cd <virtual-env-path>
source bin/activate
git clone https://github.com/vsjha18/nsetools.git
cd nsetools
make dev # package will be installed in dev mode and all the dependencies will be installed
```

[Back to Top](#nsetools)

### Running Tests

```bash
make test
```

[Back to Top](#nsetools)

### Other `make` Utilities 

Read the Makefile and find your way

[Back to Top](#nsetools)

## License

MIT License - see LICENSE file for details.

[Back to Top](#nsetools)

## Updates

To stay updated please subscribe to google group https://groups.google.com/forum/#!forum/nsetools