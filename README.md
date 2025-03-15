# NSETools

Python library for extracting data from National Stock Exchange (India)

## Table of Contents

- [Disclaimer](#disclaimer)
- [Installation](#installation)
- [Usage](#usage)
- [API Reference](#api-reference)
  - [Stock APIs](#stock-apis)
    - [Get Stock Codes](#get-stock-codes)
    - [Get Stock Quote](#get-stock-quote)
    - [Check Valid Stock Code](#check-valid-stock-code)
    - [52 Week High/Low](#52-week-highlow)
  - [Index APIs](#index-apis)
    - [Get Index Quote](#get-index-quote)
    - [Get Index List](#get-index-list)
    - [Get All Index Quotes](#get-all-index-quotes)
    - [Top Gainers & Losers](#top-gainers--losers)
    - [Advances & Declines](#advances--declines)
    - [Stocks in Index](#stocks-in-index)
  - [Derivatives APIs](#derivatives-apis)
    - [Get Future Quote](#get-future-quote)
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
   Returns a list of stock codes traded in NSE.

2. **Get Stock Quote**
   ```python
   nse.get_quote(code, all_data=False)
   ```
   - `code`: Stock symbol (e.g., 'RELIANCE')
   - `all_data`: Boolean, defaults to False. If True, returns complete response including market depth
   ```python
   # Examples
   nse.get_quote('RELIANCE')  # Basic quote
   nse.get_quote('RELIANCE', all_data=True)  # Detailed quote
   ```

3. **Check Valid Stock Code**
   ```python
   nse.is_valid_code('RELIANCE')
   ```
   Validates if given stock code exists.

4. **52 Week High/Low**
   ```python
   nse.get_52_week_high()
   nse.get_52_week_low()
   ```
   Get stocks that hit 52-week high or low.

[Back to Top](#nsetools)

### Index APIs

1. **Get Index Quote**
   ```python
   nse.get_index_quote('NIFTY 50')
   ```
   Get quote for a specific index.

2. **Get Index List**
   ```python
   nse.get_index_list()
   ```
   Returns list of all available indices.

3. **Get All Index Quotes**
   ```python
   nse.get_all_index_quote()
   ```
   Get quotes for all indices at once.

4. **Top Gainers & Losers**
   ```python
   nse.get_top_gainers(index="NIFTY")
   nse.get_top_losers(index="NIFTY")
   ```
   - `index`: Optional, defaults to "NIFTY"
   - Supported values:
     - "NIFTY" or "NIFTY 50"
     - "BANKNIFTY" or "NIFTY BANK"
     - "NIFTYNEXT50" or "NIFTY NEXT 50"
     - "SECGTR20" (Securities > ₹20)
     - "SECLWR20" (Securities < ₹20)
     - "FNO" (Futures & Options)
     - "ALL" (All Securities)

5. **Advances & Declines**
   ```python
   nse.get_advances_declines(code='nifty 50')
   ```
   - `code`: Optional, defaults to 'nifty 50'
   - Returns dict with 'advances' and 'declines' keys

6. **Stocks in Index**
   ```python
   nse.get_stocks_in_index(index="NIFTY 50")
   ```
   - `index`: Optional, defaults to "NIFTY 50"
   - Use `get_index_list()` to get valid index names

[Back to Top](#nsetools)

### Derivatives APIs

1. **Get Future Quote**
   ```python
   nse.get_future_quote('RELIANCE')
   nse.get_future_quote('RELIANCE', expiry_date='25-Jan-2024')  # For specific expiry
   ```
   - `code`: Stock symbol (e.g., 'RELIANCE')
   - `expiry_date`: Optional, format: 'DD-Mon-YYYY' (e.g., '25-Jan-2024')
   - Returns all expiries if expiry_date is None

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