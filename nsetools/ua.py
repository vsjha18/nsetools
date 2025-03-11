import requests
import random
from datetime import datetime as dt
from nsetools import urls
from time import sleep


class Session():
    __CACHE__ = {}

    def __init__(self, session_refresh_interval=60, cache_timeout=20):
        self.session_refresh_interval = session_refresh_interval
        self.cache_timeout = cache_timeout  # cache timeout in seconds
        self.create_session()
        self.flush()
    
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
        # Removed flush() call to keep cache and session management independent
    
    def flush(self):
        """Clears the URL cache"""
        self.__class__.__CACHE__ = {}

    def fetch(self, url):
        # Check cache first
        if url in self.__class__.__CACHE__:
            cache_time, response = self.__class__.__CACHE__[url]
            if (dt.now() - cache_time).seconds < self.cache_timeout:
                print("serving from cache")
                return response

        # Only check session expiry if we need to make a network request
        time_diff = dt.now() - self._session_init_time
        if time_diff.seconds >= self.session_refresh_interval:
            print("re-initing the session because of expiry")
            self.create_session()

        # Add random delay before making request
        sleep_time = random.uniform(0, 0.3)  # Random delay between 0-300ms
        print(f"Adding random delay of {sleep_time:.3f} seconds")
        sleep(sleep_time)

        # Make actual request if not in cache or cache expired
        response = self._session.get(url)
        self.__class__.__CACHE__[url] = (dt.now(), response)
        return response
