import requests 
from pprint import pprint

cookie = 'defaultLang=en; _ga=GA1.1.2026618107.1683897073; nsit=MrAFdFrQbc5U80EU5pZ0puoK; AKA_A2=A; ak_bmsc=E90480FB4227851141F18737501E4A94~000000000000000000000000000000~YAAQNtcLF4/dHDmIAQAALtZpWRPXj9fJtjTNE37NoqTbdvuvstexoDSrDf3r8rYw6TKu3r78WnjD65jrtNddbFiYnKoxpoVo2YhlsKfMO6vmBoh8QFboKhKOEHjWaNEj34rceZHCLmrCtzxbcxw/NnvRfqlgtRwpt4Q7J2nCgoIpllptsvd2b7rQziFIY62fTrMyiFIdeIZMGlqgTaefDZRwoxU46Bvyw/gZHO38LPwjjXsxxtOnSpp6FmEH6cxupbzjcMTxXyFINeiJTHfseqg31Hs0n1llaYhYI97aP4vQWtwmS27+b1qIClcgGZv9Z1m1bO6qB+c7G+4eZibXHxMSNEcZCXp7hp48diGKNz/s+A90csxBvOjQX5jWguKB7PpPr6p7cfQUWaJ8ykOSna9ulD/N7MGAk0EJOTYGZBBvuPp6on7HBym3zuHcGXidtPM6RfoLUSQDtFrE+GtGadRCMrvXjtr8ulEBQinGCbSft5Tx5QlKz8XGrKiE; nseQuoteSymbols=[{"symbol":"RELIANCE","identifier":null,"type":"equity"}]; nseappid=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJhcGkubnNlIiwiYXVkIjoiYXBpLm5zZSIsImlhdCI6MTY4NTEyOTgxNywiZXhwIjoxNjg1MTM3MDE3fQ.hSxWwxQVEo8Z-2IKY02BOrfPsb_T52U-P2tP1vkeiGg; _ga_PJSKY6CFJH=GS1.1.1685127287.2.1.1685129822.56.0.0; RT="z=1&dm=nseindia.com&si=7d261a83-6497-4b49-95e0-d20f715009eb&ss=li4xdqtg&sl=0&se=8c&tt=0&bcn=//684d0d4a.akstat.io/"; bm_sv=7EFEA6C5DF359BD32A1CF784CC137F19~YAAQBNcLF5K9jS6IAQAAkROUWRNiDyyCd+PXaoECjpNciDFiyaRbvHurFKgWS5FdWsJQjSP+seyP/1GibeOuhSJ9gVfZky1KRaOUrjcsXy2e1m3ItV3wBDWj3wXX5ojFjd/GlntlKqn9DLd9nfu4icf9di2fq/V6uvG1ATiqlSZFl2YNAMkGE3Pf3Cvtf+7bByu577NKLQGKkcVyu5ioTgWPg61A0oN8tkeB+wh5jZ+p0UriOmm2SNAteys33YrN+Fo/~1'

headers = {
    "authority": "www.nseindia.com",
    "method": "GET",
    "path": "/api/quote-equity?symbol=RELIANCE",
    "scheme": "https",
    "accept": "*/*",
    "accept-encoding" : "gzip, deflate, br",
    "accept-language" : "en-US,en;q=0.9,hi;q=0.8",
    "cookie": cookie,
    "referrer": "https://www.nseindia.com/get-quotes/equity?symbol=RELIANCE",
    "sec-ch-ua": '"Chromium";v="112", "Google Chrome";v="112", "Not:A-Brand";v="99"',
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": "macOS",
    "sec-fetch-dest": "empty",
    "sec-fetch-mode": "cors",
    "sec-fecth-site": "same-origin",
    "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36",
}

s = requests.Session()
only_ua = {"user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36"}
base_url = "https://nseindia.com"
web_url = "https://www.nseindia.com/get-quotes/equity?symbol=RELIANCE"
api_url = "https://www.nseindia.com/api/quote-equity?symbol=RELIANCE"
url2 = "https://www.nseindia.com/api/quote-equity?symbol=RELIANCE&section=trade_info"
#res = requests.get(url, headers=headers)
#pprint(res.content.decode("utf-8"))