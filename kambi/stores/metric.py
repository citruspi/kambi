#!/usr/bin/env python
# -*- coding utf-8 -*-

import time
import multiprocessing


class MetricStore(dict):

    def __init__(self, metric, *args, **kwargs):
        self.metric = metric
        self.prune_lock = False

        if self.metric.prune:
            process = multiprocessing.Process(target=self.prune)
            process.start()

        super().__init__(*args, **kwargs)

    def __getitem__(self, key):
        return super().__getitem__(key)

    def __setitem__(self, key, value):
        try:
            if self[key] == value:
                print('Skipping {}'.format(key))
                return
            else:
                print('Updating {}'.format(key))
        except KeyError:
            print('Setting {}'.format(key))
            pass

        self.metric.update(int(key)/1000, value)
        super().__setitem__(key, value)

    def update(self, *args, **kwargs):
        for k, v in dict(*args, **kwargs).items():
            self[k] = v

    def prune(self):
        while True:
            if not self.prune_lock:
                print('Prune lock disabled')
                for key in self:
                    if int(key) < int(time.time() * 1000) - self.metric.span:
                        print('Deleting {}'.format(key))
                        del key
                    else:
                        print('Keeping {}'.format(key))
                time.sleep(self.metric.span/1000)
            else:
                print('Prune lock enabled')
                time.sleep(60)
