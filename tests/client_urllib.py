import urllib.request
home_url = "https://nseindia.com"
api_url = "https://www.nseindia.com/api/quote-equity?symbol=RELIANCE"
# import ipdb; ipdb.set_trace()
opener = urllib.request.build_opener()
opener.addheaders = [("user-agent", "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36")]
response = opener.open(home_url)
