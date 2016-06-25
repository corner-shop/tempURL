#!/usr/bin/env python -tt -u

from hypothesis import given
from hypothesis.strategies import text
import unittest
import os
import time
import requests
import json

class TestStringMethods(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        os.system('docker-compose build')
        os.system('docker-compose down')
        os.system('docker-compose up -d')
        time.sleep(10)

    @classmethod
    def tearDownClass(cls):
        os.system('docker-compose down')

    @given(text(min_size=1))
    def test_not_null_upload_returns_200(self, s):
        payload={'tempurl': s,
                 'data': s}

        r = requests.post('http://172.17.0.1:6222/upload',json=payload)
        assert r.status_code == 200

    @given(text(min_size=0, max_size=0))
    def test_null_upload_returns_415(self, s):
        payload={'tempurl': s,
                 'data': s}

        r = requests.post('http://172.17.0.1:6222/upload',json=payload)
        assert r.status_code == 415

    @given(text(min_size=1))
    def test_not_null_download_returns_200(self, s):
        payload={'tempurl': s,
                 'data': s}

        r = requests.post('http://172.17.0.1:6222/upload',json=payload)
        payload={'tempurl': s}
        r = requests.get('http://172.17.0.1:6222/download',json=payload)
        print r.status_code
        assert r.status_code == 200

    @given(text(min_size=0, max_size=0))
    def test_null_download_returns_415(self, s):
        payload={'tempurl': s}
        r = requests.get('http://172.17.0.1:6222/download',json=payload)
        assert r.status_code == 415


if __name__ == '__main__':
    unittest.main()