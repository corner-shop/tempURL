#!/usr/bin/env python -tt -u

from hypothesis import (given, example)
from hypothesis.strategies import (text, integers)
import unittest
import os
import time
import requests
import StringIO
import re
import string

ALPHABET = "0123456789abcdefghijklmnopqrstuvxyzABCDEFGHIJKLMNOPQRSTUVXYZ_-"

class TestStringMethods(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        os.system('docker-compose build')
        os.system('docker-compose down')
        os.system('docker-compose rm -f')
        os.system('docker-compose up -d')
        time.sleep(10)

    @classmethod
    def tearDownClass(cls):
        os.system('docker-compose down')
        os.system('docker-compose rm -f')
        pass


    @given(
        tempurl=integers(min_value=0, max_value=300),
        ttl=integers(min_value=300),
        data=text(min_size=1, max_size=128)
    )
    def test_post_should_not_take_an_int_as_tempurl(self, tempurl, ttl, data):
        f = StringIO.StringIO(data)
        files = {'file': f }
        url = 'http://127.0.0.1:6222/api'
        values = {'tempurl': tempurl, 'ttl': ttl}

        r = requests.post(url, files=files, params=values)
        assert r.status_code == 400


    @given(
        tempurl=text(alphabet=ALPHABET, min_size=0, max_size=3),
        ttl=integers(min_value=1, max_value=65535),
        data=text(min_size=1, max_size=128)
    )
    def test_post_should_not_take_less_than_4_chars_as_tempurl(self, tempurl, ttl, data):
        f = StringIO.StringIO(data)
        files = {'file': f }
        url = 'http://127.0.0.1:6222/api'
        values = {'tempurl': tempurl, 'ttl': ttl}

        r = requests.post(url, files=files, params=values)
        assert r.status_code == 400


    @given(
        tempurl=text(alphabet=ALPHABET, min_size=5, max_size=128),
        ttl=integers(min_value=0, max_value=65535),
        data=text(min_size=1, max_size=128)
    )
    def test_post_ttl_smaller_than_65536_should_return_201(self, tempurl, ttl, data):
        f = StringIO.StringIO(data)
        files = {'file': f }
        url = 'http://127.0.0.1:6222/api'
        values = {'tempurl': tempurl, 'ttl': ttl}

        r = requests.post(url, files=files, params=values)
        assert r.status_code == 201


    @given(
        tempurl=text(alphabet=ALPHABET, min_size=5, max_size=128),
        ttl=integers(min_value=65536, max_value=99999),
        data=text(min_size=1, max_size=128)
    )
    def test_post_ttl_higher_than_65536_should_return_400(self, tempurl, ttl, data):
        f = StringIO.StringIO(data)
        files = {'file': f }
        url = 'http://127.0.0.1:6222/api'
        values = {'tempurl': tempurl, 'ttl': ttl}

        r = requests.post(url, files=files, params=values)
        assert r.status_code == 400


    @given(
        tempurl=text(alphabet=ALPHABET, min_size=5, max_size=128),
        ttl=integers(min_value=300, max_value=65535),
        data=text(min_size=1, max_size=128)
    )
    def test_post_should_take_more_than_4_chars_as_tempurl(self, tempurl, ttl, data):
        f = StringIO.StringIO(data)
        files = {'file': f }
        url = 'http://127.0.0.1:6222/api'
        values = {'tempurl': tempurl, 'ttl': ttl}

        r = requests.post(url, files=files, params=values)
        assert r.status_code == 201

    @given(
        tempurl=text(alphabet=ALPHABET, max_size=0),
        ttl=integers(min_value=300, max_value=65535),
        data=text(min_size=1, max_size=128)
    )
    def test_post_should_not_accept_an_emptry_string_as_tempurl(self, tempurl, ttl, data):
        f = StringIO.StringIO(data)
        files = {'file': f }
        url = 'http://127.0.0.1:6222/api'
        values = {'tempurl': tempurl, 'ttl': ttl}

        r = requests.post(url, files=files, params=values)
        assert r.status_code == 400

    @given(
        tempurl=text(alphabet=ALPHABET, min_size=4, max_size=4),
        ttl=integers(min_value=300, max_value=65535),
        data=text(max_size=0)
    )
    def test_post_should_not_accept_empty_string_for_data(self, tempurl, ttl, data):
        f = StringIO.StringIO(data)
        files = {'file': f }
        url = 'http://127.0.0.1:6222/api'
        values = {'tempurl': tempurl, 'ttl': ttl}

        r = requests.post(url, files=files, params=values)
        assert r.status_code == 400


    @given(
        tempurl=text(min_size=0, max_size=128),
        ttl=integers(min_value=300, max_value=65535),
        data=text(max_size=128)
    )
    def test_post_random_tempurl(self, tempurl, ttl, data):

        f = StringIO.StringIO(data)
        files = {'file': f }
        url = 'http://127.0.0.1:6222/api'
        values = {'tempurl': tempurl, 'ttl': ttl}

        r = requests.post(url, files=files, params=values)

        # hypothesis will generate invalid strings for the tempurl
        # we expect the code to reject them with a 404.
        if not re.match("^[A-Za-z0-9_-]{4,}$", str(tempurl.encode('utf-8'))):
            assert r.status_code == 400
        else:
            assert r.status_code == 201


    @given(
        tempurl=text(alphabet=ALPHABET, min_size=4, max_size=128),
        ttl=integers(min_value=300, max_value=65535),
        data=text(min_size=1, max_size=128)
    )
    def test_post_random_data_block(self, tempurl, ttl, data):

        f = StringIO.StringIO(data)
        files = {'file': f }
        url = 'http://127.0.0.1:6222/api'
        values = {'tempurl': tempurl, 'ttl': ttl}

        r = requests.post(url, files=files, params=values)
        assert r.status_code == 201


    @given(
        tempurl=text(alphabet=ALPHABET, min_size=4, max_size=128),
        ttl=integers(min_value=300, max_value=65535),
        data=text(alphabet=ALPHABET, min_size=1, max_size=128)
    )
    def test_get_matches_upload(self, tempurl, ttl, data):

        # upload random file
        f = StringIO.StringIO(data)
        files = {'file': f }
        url = 'http://127.0.0.1:6222/api'
        values = {'tempurl': tempurl, 'ttl': ttl}

        r = requests.post(url, files=files, params=values)

        # download uploaded file
        values = { 'tempurl': tempurl }

        r = requests.get(url, params=values)
        # and that our download actually matches our upload
        assert r.content == data


    def test_get_expires_after_ttl(self):
        tempurl = 'kjasdkfasdf'
        data = 'adsfadsf'
        ttl = 1

        # upload random file
        f = StringIO.StringIO(data)
        files = {'file': f }
        url = 'http://127.0.0.1:6222/api'
        values = {'tempurl': tempurl, 'ttl': ttl}

        r = requests.post(url, files=files, params=values)

        # download uploaded file
        values = { 'tempurl': tempurl }

        time.sleep(2)
        r = requests.get(url, params=values)
        assert r.status_code == 404

    def test_health_endpoint(self):
        url = 'http://127.0.0.1:6222/health'

        r = requests.get(url)
        assert r.status_code == 200


if __name__ == '__main__':
    unittest.main()
