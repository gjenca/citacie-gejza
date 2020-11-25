#!/usr/bin/env python3
import yaml
import sys
from _yadata_types import MyOwn,Citation
from snip import get_snip 

l=yaml.load_all(sys.stdin,Loader=yaml.Loader)
for obj in l:
    if 'journal' in obj:
        obj['snip']=get_snip(obj['journal'],obj['year'])
    print('---')
    sys.stdout.write(yaml.dump(obj,allow_unicode=True,sort_keys=False,default_flow_style=None))

        


