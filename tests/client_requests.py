import requests
home_url = "https://nseindia.com"
api_url = "https://www.nseindia.com/api/quote-equity?symbol=RELIANCE"
# import ipdb; ipdb.set_trace()
s = requests.Session()
headers = {"user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36"}
headers = {"Accept": "*/*",
            "Accept-Language": "en-US,en;q=0.5",
                "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36",
                "X-Requested-With": "XMLHttpRequest"
                }

s.headers.update(headers)
res1 = s.get(home_url)
res2 = s.get(api_url)
print(res2.content)
