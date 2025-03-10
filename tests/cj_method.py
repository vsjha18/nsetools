from urllib.request import build_opener, HTTPCookieProcessor, Request
from http.cookiejar import CookieJar
from urllib.parse import urlencode
home_url = "https://nseindia.com"
api_url = "https://www.nseindia.com/api/quote-equity?symbol=RELIANCE"
headers = {"user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36"}
headers = {'Accept': '*/*',
                'Accept-Language': 'en-US,en;q=0.5',
                'Host': 'www1.nseindia.com',
                'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:28.0) Gecko/20100101 Firefox/28.0',
                'X-Requested-With': 'XMLHttpRequest'
                }
# import ipdb; ipdb.set_trace()
cj = CookieJar()
opener = build_opener(HTTPCookieProcessor(cj))
req = Request(home_url, None, headers=headers)
res = opener.open(req)
