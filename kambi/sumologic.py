#!/usr/bin/env python
# -*- coding: utf-8 -*-

import requests


class Client(object):

    def __init__(self, user, token):
        self.conn = requests.Session()
        self.conn.auth = (user, token)
        self.conn.headers = {
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        }

    def get(self, endpoint, *args, **kwargs):
        return self.conn.get(endpoint, *args, **kwargs)
