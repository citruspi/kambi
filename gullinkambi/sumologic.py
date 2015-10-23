#!/usr/bin/env python
# -*- coding: utf-8 -*-

import time
import requests


class Client(object):

    def __init__(self, user, token):
        self.conn = requests.Session()
        self.conn.auth = (user, token)
        self.conn.headers = {
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        }

    def search(self, query, from_timestamp=None, to_timestamp=None):
        from_timestamp = from_timestamp or int(time.time() * 1000)-900000
        to_timestamp = to_timestamp or int(time.time() * 1000)

        endpoint = 'https://api.us2.sumologic.com/api/v1/logs/search'

        params = {
            'q': query,
            'from': from_timestamp,
            'to': to_timestamp,
            'tz': 'Etc/UTC',
            'format': 'json'
        }

        r = self.conn.get(endpoint, params=params)

        r.raise_for_status()

        return r.json()
