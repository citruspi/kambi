#!/usr/bin/env python
# -*- coding utf-8 -*-


class MetricStore(dict):

    def __init__(self, metric, *args, **kwargs):
        self.metric = metric

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
