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
    - [Stocks in Index](#6-stocks-in-index)
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
   Returns list of stock codes traded in NSE.
   ```python
   >>> codes = nse.get_stock_codes()
   >>> print(codes[:5])
   ['20MICRONS', '3IINFOTECH', '3MINDIA', '3PLAND', '63MOONS']
   ```

2. **Get Stock Quote**
   ```python
   nse.get_quote(code, all_data=False)
   ```
   Gets real-time or delayed quote data for a given stock.
   - `code`: NSE stock symbol (e.g., 'RELIANCE')
   - `all_data`: If True returns complete quote data, if False returns only price info
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
   nse.is_valid_code('RELIANCE')
   ```
   Validates if given stock code exists.
   ```python
   >>> nse.is_valid_code("INFY")
   True
   >>> nse.is_valid_code("INVALID")
   False
   ```

4. **52 Week High/Low**
   ```python
   nse.get_52_week_high()
   nse.get_52_week_low()
   ```
   Get stocks that hit 52-week high or low.
   ```python
   >>> nse.get_52_week_high()
   [{
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
   {...}]

   >>> nse.get_52_week_low()  # Similar structure as 52-week high
   ```

[Back to Top](#nsetools)

### Index APIs

1. **Get Index Quote**
   ```python
   nse.get_index_quote(index="NIFTY 50")
   ```
   Gets detailed quote information for a given index.
   ```python
   {
       'key': 'BROAD MARKET INDICES',
       'index': 'NIFTY 50', 
       'last': 22508.75,
       'variation': 111.55,
       'percentChange': 0.5,
       # ... additional fields
   }
   ```

2. **Get Index List**
   ```python
   nse.get_index_list()
   ```
   Gets list of all NSE index symbols.

3. **Get All Index Quotes**
   ```python
   nse.get_all_index_quote()
   ```
   Gets quotes and information for all available indices in a single API call.

4. **Top Gainers & Losers**
   ```python
   nse.get_top_gainers(index="NIFTY")
   nse.get_top_losers(index="NIFTY")
   ```
   Gets real-time data for stocks with highest gains/losses.
   - Supported indices: NIFTY (default), BANKNIFTY, NIFTYNEXT50, SecGtr20, SecLwr20, FNO, ALL

5. **Advances & Declines**
   ```python
   nse.get_advances_declines(index='nifty 50')
   ```
   Gets number of advancing and declining stocks in an index.
   ```python
   >>> nse.get_advances_declines("NIFTY BANK")
   {'advances': 7, 'declines': 4}
   ```

6. **Stocks in Index**
   ```python
   nse.get_stocks_in_index(index="NIFTY 50")
   nse.get_stock_quote_in_index(index="NIFTY 50", include_index=False)
   ```
   - `get_stocks_in_index`: Gets list of stock symbols in an index
   - `get_stock_quote_in_index`: Gets detailed quotes for all stocks in an index
     - `include_index`: If True, includes index quote in results

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
   [{'expiryDate': '27-Mar-2025',
     'lastPrice': 1246,
     'premium': 4.45,
     'openInterest': 257812,
     # ... additional fields
   }]
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