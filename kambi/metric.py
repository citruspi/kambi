#!/usr/bin/env python
# -*- coding: utf-8 -*-

import time
import kambi.query
import kambi.stores.metric


class Metric(object):
    def __init__(self, metric_id, query, sumologic_client, statuspageio_client,
                 interval=30, span=900000, prune=True):
        self.metric_id = metric_id
        self.interval = interval
        self.conn = statuspageio_client
        self.span = span
        self.prune = prune

        query['conn'] = sumologic_client
        query['span'] = span
        self.query = kambi.query.Query(**query)

        self.datastore = kambi.stores.metric.MetricStore(self)

    def populate(self):
        while True:
            started = int(time.time() * 1000)

            self.datastore.update(self.query.fetch())

            finished = int(time.time() * 1000)

            time_left = (self.interval * 1000 - (finished - started))

            if time_left > 0:
                time.sleep(time_left / 1000)

    def update(self, timestamp, value):
        self.conn.update_metric(self.metric_id, timestamp, value)
