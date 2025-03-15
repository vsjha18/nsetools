"""
URL constants for NSE related operations
"""

# Base URLs
NSE_HOME = "https://nseindia.com"
NSE_MAIN = "https://www.nseindia.com"
NSE_LEGACY = "https://www1.nseindia.com"

# Quote URLs
QUOTE_EQUITY_URL = f"{NSE_MAIN}/get-quotes/equity?symbol=%s"
QUOTE_API_URL = f"{NSE_MAIN}/api/quote-equity?symbol=%s"

# Stock list URLs
STOCKS_CSV_URL = f"https://nsearchives.nseindia.com/content/equities/EQUITY_L.csv"

# Market movers URLs
TOP_GAINERS_URL = f"{NSE_MAIN}/api/live-analysis-variations?index=gainers"
TOP_LOSERS_URL = f"{NSE_MAIN}/api/live-analysis-variations?index=loosers"
TOP_FNO_GAINER_URL = f"{NSE_LEGACY}/live_market/dynaContent/live_analysis/gainers/fnoGainers1.json"
TOP_FNO_LOSER_URL = f"{NSE_LEGACY}/live_market/dynaContent/live_analysis/losers/fnoLosers1.json"
FIFTYTWO_WEEK_HIGH_URL = f"{NSE_MAIN}/api/live-analysis-data-52weekhighstock"
FIFTYTWO_WEEK_LOW_URL = f"{NSE_MAIN}/api/live-analysis-data-52weeklowstock"

# Index URLs
ALL_INDICES_URL = f"{NSE_MAIN}/api/allIndices"
STOCKS_IN_INDEX_URL = f"{NSE_MAIN}/api/equity-stockIndices?index=%s"


# Historical data URLs
BHAVCOPY_BASE_URL = f"{NSE_LEGACY}/content/historical/EQUITIES/%s/%s/cm%s%s%sbhav.csv.zip"
BHAVCOPY_BASE_FILENAME = "cm%s%s%sbhav.csv"

# Drivative URLs
QUOTE_DRIVATIVE_URL = f"{NSE_MAIN}/api/quote-derivative?symbol=%s"
