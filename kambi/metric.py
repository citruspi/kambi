#!/usr/bin/env python
# -*- coding: utf-8 -*-

import time
import kambi.query


class Metric(object):
    def __init__(self, metric_id, query, sumologic_client, statuspageio_client,
                 interval=30):
        self.metric_id = metric_id
        self.interval = interval
        self.clients = {
            'statuspageio': statuspageio_client
        }

        query['conn'] = sumologic_client
        self.query = kambi.query.Query(**query)

    def populate(self):
        while True:
            started = int(time.time() * 1000)

            print(self.query.fetch())

            finished = int(time.time() * 1000)

            time_left = (self.interval * 1000 - (finished - started))

            if time_left > 0:
                time.sleep(time_left / 1000)