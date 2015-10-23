#!/usr/bin/env python
# -*- coding: utf-8 -*-

import time
import requests


class Client(object):

    def __init__(self, token, page_id):
        self.conn = requests.Session()
        self.conn.headers = {
            'Content-Type': 'application/x-www-form-urlencoded',
            'Authorization': 'OAuth {}'.format(token)
        }

        self.page_id = page_id

    def post_metric_data(self, metric_id, data, keys=None):
        keys = keys or {
            'timestamp': '_timeslice',
            'value': 'value'
        }

        endpoint = 'https://api.statuspage.io/v1/pages/{page}/metrics/' \
            '{metric}/data.json'
        endpoint = endpoint.format(page=self.page_id, metric=metric_id)

        for point in data:
            backoff = 1

            data = {
                'data[timestamp]': int(point[keys['timestamp']])/1000,
                'data[value]': point[keys['value']]
            }

            while True:
                r = self.conn.post(endpoint, data=data)

                try:
                    r.raise_for_status()
                    break
                except Exception as e:
                    if r.status_code == 420:
                        time.sleep(backoff)
                        backoff += backoff
                    else:
                        raise e
