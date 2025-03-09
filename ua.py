import requests
from datetime import datetime as dt
from nsetools import urls


class Session():
    def __init__(self, session_refresh_interval=60):
        self.session_refresh_interval = session_refresh_interval
        self.create_session()
    
    def nse_headers(self):
        """
        Builds right set of headers for requesting http://nseindia.com
        :return: a dict with http headers
        """
        return {"Accept": "*/*",
                "Accept-Language": "en-US,en;q=0.5",
                "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36",
                "X-Requested-With": "XMLHttpRequest"
                }
    
    def create_session(self):
        home_url = "https://nseindia.com"
        self._session = requests.Session()
        self._session.headers.update(self.nse_headers())
        self._session.get(urls.NSE_HOME)
        self._session_init_time = dt.now()        
    
    def fetch(self, url):
        time_diff = dt.now() - self._session_init_time
        if time_diff.seconds < self.session_refresh_interval:
            print("time diff is ", time_diff.seconds)
            return self._session.get(url)
        else:
            print("time diff is ", time_diff.seconds)
            print("re-initing the session because of expiry")
            self.create_session()
            return self._session.get(url)
