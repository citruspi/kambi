#!/usr/bin/env python
# -*- coding: utf-8 -*-

import time
import os.path


class Metric(object):
    def __init__(self, metric_id, query, sumologic_client, statuspageio_client,
                 interval=30):
        query['timestamp'] = query['timestamp'] or '_timeslice'
        query['value'] = query['value'] or 'value'

        if query['template']:
            path = os.path.join(
                os.path.expanduser('~'),
                '.kambi/templates',
                query['template'])

            with open(path, 'r') as f:
                query['raw'] = f.read()

        self.metric_id = metric_id
        self.query = query
        self.interval = interval
        self.clients = {
            'sumologic': sumologic_client,
            'statuspageio': statuspageio_client
        }

    def populate(self):
        keys = {
            'timestamp': self.query['timestamp'],
            'value': self.query['value']
        }

        while True:
            started = int(time.time() * 1000)

            data = self.clients['sumologic'].search(self.query['raw'])
            self.clients['statuspageio'].post_metric_data(self.metric_id, data,
                                                          keys)

            finished = int(time.time() * 1000)

            time_left = (self.interval * 1000 - (finished - started))

            if time_left > 0:
                time.sleep(time_left / 1000)
