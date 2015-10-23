#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
import os.path
import gullinkambi.sumologic
import gullinkambi.statuspageio
import gullinkambi.metric


class Gullinkambi(object):
    def __init__(self):
        config_path = os.path.join(
            os.path.expanduser('~'),
            '.gullinkambi',
            'config.json')

        with open(config_path, 'r') as f:
            self.config = json.load(f)

        sumologic_client = gullinkambi.sumologic.Client(
            **self.config['auth']['sumologic'])

        statuspageio_client = gullinkambi.statuspageio.Client(
            **self.config['auth']['statuspageio'])

        self.metrics = []

        for metric in self.config['metrics']:
            self.metrics.append(gullinkambi.metric.Metric(**{
                'metric_id': metric['id'],
                'query': metric['query'],
                'sumologic_client': sumologic_client,
                'statuspageio_client': statuspageio_client,
                'interval': metric['interval']
            }))
