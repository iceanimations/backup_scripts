import json
import os
import sys
import time

config_file = os.path.join( os.path.dirname(__file__), 'config.json' )

with open(config_file) as f:
    data = json.load(f)

module = sys.modules[__name__]
for key, value in data.items():
    setattr(module, key, value)

def getNowString(now=None):
    if not now:
        now = time.localtime(time.time())
    nowstring = time.strftime( "%Y-%m-%d_%H-%M", now)
    return nowstring

