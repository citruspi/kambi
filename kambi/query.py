#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os.path
import time


class Query(object):

    endpoint = 'https://api.us2.sumologic.com/api/v1/logs/search'

    def __init__(self, template, conn, timestamp='_timeslice', value='value'):
        template_path = os.path.join(os.path.expanduser('~'),
                                     '.kambi/templates',
                                     template)

        with open(template_path, 'r') as f:
            self.query = f.read()

        self.conn = conn
        self.timestamp = timestamp
        self.value = value

    def fetch(self, from_timestamp=None, to_timestamp=None):
        from_timestamp = from_timestamp or int(time.time() * 1000)-900000
        to_timestamp = to_timestamp or int(time.time() * 1000)

        params = {
            'q': self.query,
            'from': from_timestamp,
            'to': to_timestamp,
            'tz': 'Etc/UTC',
            'format': 'json'
        }

        r = self.conn.get(self.endpoint, params=params)

        r.raise_for_status()

        data = r.json()

        data = {x[self.timestamp]: x[self.value] for x in data}

        return data
