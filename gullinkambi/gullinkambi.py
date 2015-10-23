#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
import os.path


class Gullinkambi(object):
    def __init__(self):
        config_path = os.path.join(
            os.path.expanduser('~'),
            '.gullinkambi',
            'config.json')

        with open(config_path, 'r') as f:
            self.config = json.load(f)
