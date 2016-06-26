#!/usr/bin/env python -tt -u

from hypothesis import (given, example)
from hypothesis.strategies import (text, integers)
import unittest
import os
import time
import requests
import StringIO
import re

class TestStringMethods(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        os.system('docker build -t azulinho/tempurl .')
        os.system('docker-compose down')
        os.system('docker-compose up -d')
        time.sleep(10)

    @classmethod
    def tearDownClass(cls):
        os.system('docker-compose down')

    @given(text(min_size=0), integers(min_value=300), text(min_size=0))
    @example('',1,'')
    @example(0,1,0)
    @example('000000',1,'000000')
    def test_post(self, tempurl, ttl, data):

        f = StringIO.StringIO(data)
        files = {'file': f }
        url = 'http://172.17.0.1:6222/api'
        values = {'tempurl': tempurl, 'ttl': ttl}

        r = requests.post(url, files=files, params=values)

        # code should not accept an int as an url
        if not isinstance(tempurl, basestring):
            assert r.status_code == 404
        else:
            # code should not accept an empty string as an url
            if len(tempurl) == 0:
                assert r.status_code == 404
            else:
                # hypothesis will generate invalid strings for the tempurl
                # we expect the code to reject them with a 404.
                if not re.match("^[A-Za-z0-9_-]{4,}$", str(tempurl.encode('utf-8'))):
                    assert r.status_code == 404
                else:
                    assert r.status_code == 200

    @given(text(min_size=0), integers(min_value=300), text(min_size=0))
    @example('',1,'')
    @example(0,1,0)
    @example('000000',1,'000000')
    def test_get_matches_upload(self, tempurl, ttl, data):

        # upload random file
        f = StringIO.StringIO(data)
        files = {'file': f }
        url = 'http://172.17.0.1:6222/api'
        values = {'tempurl': tempurl, 'ttl': ttl}

        r = requests.post(url, files=files, params=values)

        # download uploaded file
        values = { 'tempurl': tempurl }

        r = requests.get(url, params=values)

        # code should not accept an int as an url
        if not isinstance(tempurl, basestring):
            assert r.status_code == 404
        else:
            # code should not accept an empty string as an url
            if len(tempurl) == 0:
                assert r.status_code == 404
            else:
                # hypothesis will generate invalid strings for the tempurl
                # we expect the code to reject them with a 404.
                if not re.match("^[A-Za-z0-9_-]{4,}$", str(tempurl.encode('utf-8'))):
                    assert r.status_code == 404
                else:
                    # expect a successull download
                    assert r.status_code == 200
                    # and that our download actually matches our upload
                    assert r.content == data
                    # a second download request should return a 404
                    r = requests.get(url, params=values)
                    assert r.status_code == 404

    def test_get_expires_after_ttl(self):
        tempurl = 'kjasdkfasdf'
        data = 'adsfadsf'
        ttl = 1

        # upload random file
        f = StringIO.StringIO(data)
        files = {'file': f }
        url = 'http://172.17.0.1:6222/api'
        values = {'tempurl': tempurl, 'ttl': ttl}

        r = requests.post(url, files=files, params=values)

        # download uploaded file
        values = { 'tempurl': tempurl }

        time.sleep(2)
        r = requests.get(url, params=values)
        assert r.status_code == 404


if __name__ == '__main__':
    unittest.main()