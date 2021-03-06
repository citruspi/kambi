#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
import multiprocessing
import os.path
import kambi.sumologic
import kambi.statuspageio
import kambi.metric
import time
import random


class Kambi(object):
    def __init__(self):
        config_path = os.path.join(
            os.path.expanduser('~'),
            '.kambi',
            'config.json')

        with open(config_path, 'r') as f:
            self.config = json.load(f)

        sumologic_client = kambi.sumologic.Client(
            **self.config['auth']['sumologic'])

        statuspageio_client = kambi.statuspageio.Client(
            **self.config['auth']['statuspageio'])

        self.metrics = []

        for metric in self.config['metrics']:
            self.metrics.append(kambi.metric.Metric(**{
                'metric_id': metric['id'],
                'query': metric['query'],
                'sumologic_client': sumologic_client,
                'statuspageio_client': statuspageio_client,
                'interval': metric['interval'],
                'span': metric['span'],
                'backfill': metric['backfill'],
                'backfill_span': metric['backfill_span']
            }))

    def start(self):
        for metric in self.metrics:
            time.sleep(random.randint(5, 15))
            process = multiprocessing.Process(target=metric.populate)
            process.start()
