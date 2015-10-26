#!/usr/bin/env python
# -*- coding: utf-8 -*-

import requests
import time


class Client(object):

    backoff = 0.1

    def __init__(self, user, token):
        self.conn = requests.Session()
        self.conn.auth = (user, token)
        self.conn.headers = {
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        }

    def get(self, endpoint, *args, **kwargs):
        while True:
            r = self.conn.get(endpoint, *args, **kwargs)

            try:
                r.raise_for_status()
                self.backoff = 0.1
                return r
            except Exception as e:
                if r.status_code in [408, 420, 500, 501, 502, 503, 504]:
                    message = 'Recieved {code} from Sumo. Sleeping for {time}'
                    print(message.format(code=r.status_code, time=self.backoff))
                    time.sleep(self.backoff)
                    self.backoff += self.backoff
                else:
                    raise e
