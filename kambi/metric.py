#!/usr/bin/env python
# -*- coding: utf-8 -*-

import time
import kambi.query
import kambi.stores.metric
import multiprocessing


class Metric(object):
    def __init__(self, metric_id, query, sumologic_client, statuspageio_client,
                 interval=30, span=900000, prune=True, backfill=False,
                 backfill_span=86400000):
        self.metric_id = metric_id
        self.interval = interval
        self.conn = statuspageio_client
        self.span = span
        self.prune = prune

        query['conn'] = sumologic_client
        query['span'] = span
        self.query = kambi.query.Query(**query)

        self.datastore = kambi.stores.metric.MetricStore(self)

        if backfill:
            process = multiprocessing.Process(target=self.backfill,
                                              args=(backfill_span,))
            process.start()

    def populate(self):
        while True:
            started = int(time.time() * 1000)

            self.datastore.update(self.query.fetch())

            finished = int(time.time() * 1000)

            time_left = (self.interval * 1000 - (finished - started))

            if time_left > 0:
                time.sleep(time_left / 1000)

    def backfill(self, backfill_span):
        print('Starting backfill')

        start = int(time.time() * 1000)

        prune_lock_value = self.datastore.prune_lock
        self.datastore.prune_lock = True

        while start > start - backfill_span:
            from_ = start - backfill_span
            to = start

            print('Backfilling from {from_} to {to}'.format(from_=from_,
                                                            to=to))
            self.datastore.update(self.query.fetch(from_, to))

            start -= self.span

        self.datastore.prune_lock = prune_lock_value

        print('Finished backfill')

    def update(self, timestamp, value):
        self.conn.update_metric(self.metric_id, timestamp, value)
