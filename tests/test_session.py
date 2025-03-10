import unittest
import requests
import time
import sys
import os
from datetime import datetime as dt
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from nsetools.ua import Session
from nsetools import urls

class TestSession(unittest.TestCase):
    def setUp(self):
        self.session = Session(session_refresh_interval=2)  # Short interval for testing

    def test_session_headers(self):
        """Test if proper headers are set"""
        headers = self.session.nse_headers()
        essential_headers = [
            "Accept", "Accept-Language", "user-agent", "X-Requested-With"
        ]
        for header in essential_headers:
            self.assertIn(header, headers)
        self.assertIsInstance(headers, dict)

    def test_session_creation(self):
        """Test if session is created with proper attributes"""
        self.assertIsInstance(self.session._session, requests.Session)
        self.assertIsInstance(self.session._session_init_time, dt)
        self.assertEqual(self.session.session_refresh_interval, 2)

    def test_session_refresh(self):
        """Test if session refreshes after interval"""
        initial_time = self.session._session_init_time
        initial_session_id = id(self.session._session)
        
        response = self.session.fetch(urls.NSE_HOME)
        self.assertEqual(response.status_code, 200)
        
        time.sleep(3)  # Wait longer than refresh interval
        
        response = self.session.fetch(urls.NSE_HOME)
        self.assertEqual(response.status_code, 200)
        
        # Verify session object was recreated
        self.assertNotEqual(id(self.session._session), initial_session_id)
        
        # Verify timestamp was updated
        self.assertNotEqual(initial_time, self.session._session_init_time)
        self.assertGreater(self.session._session_init_time, initial_time)

    def test_session_reuse(self):
        """Test if session is reused within refresh interval"""
        response1 = self.session.fetch(urls.NSE_HOME)
        initial_time = self.session._session_init_time
        
        response2 = self.session.fetch(urls.NSE_HOME)
        self.assertEqual(initial_time, self.session._session_init_time)
        
        self.assertEqual(response1.status_code, 200)
        self.assertEqual(response2.status_code, 200)

if __name__ == '__main__':
    unittest.main()
