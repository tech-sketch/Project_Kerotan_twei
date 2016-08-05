# -*- coding: UTF-8 -*-
# APIkey_load_yaml.py

import yaml
import pprint
import sys
import os
API_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)))


def get_API_key(name):
    try:
        # with open(os.path.dirname(os.path.abspath(__file__)) + u"/API_KEY.yaml", "r") as f:
        with open(os.path.join(API_DIR, u"API_KEY.yaml"), "r") as f:
            data = yaml.load(f)[name]["key"]
            # pprint.pprint(data)
            return data
    except:
        print('load yaml error')
        raise

if __name__ == '__main__':
    print(get_API_key("TEST"))
