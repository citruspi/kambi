#!/usr/bin/env python
# -*- coding: utf-8 -*-

import time
import requests


class Client(object):

    backoff = 0.01
    api_base = 'https://api.statuspage.io/v1/pages/{page}'

    def __init__(self, token, page_id):
        self.conn = requests.Session()
        self.conn.headers = {
            'Content-Type': 'application/x-www-form-urlencoded',
            'Authorization': 'OAuth {}'.format(token)
        }

        self.page_id = page_id
        self.api_base = self.api_base.format(page=page_id)

    def update_metric(self, metric_id, timestamp, value):
        endpoint = '{api_base}/metrics/{metric}/data.json'
        endpoint = endpoint.format(api_base=self.api_base, metric=metric_id)

        data = {
            'data[timestamp]': timestamp,
            'data[value]': value
        }

        while True:
            r = self.conn.post(endpoint, data=data)

            try:
                r.raise_for_status()
                self.backoff = 0.01
                break
            except Exception as e:
                if r.status_code in [408, 420, 500, 501, 502, 503, 504]:
                    message = 'Recieved {code} from StatusPage. Sleeping for {time}'
                    print(message.format(code=r.status_code, time=self.backoff))

                    time.sleep(self.backoff)
                    self.backoff += self.backoff
                else:
                    raise e
