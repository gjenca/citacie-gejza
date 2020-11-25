#!/usr/bin/env python3
import yaml
import sys
from _yadata_types import MyOwn

l=yaml.load_all(sys.stdin)
for d in l:
    del d['key']
    if d['myown']:
        del d['myown']
        print('---')
        sys.stdout.write(yaml.dump(MyOwn(d),allow_unicode=True,sort_keys=False,default_flow_style=None))
