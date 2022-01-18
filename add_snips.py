#!/usr/bin/env python3
import yaml
import sys
from _yadata_types import MyOwn,Citation,Review
from snip import get_snip 

l=yaml.load_all(sys.stdin,Loader=yaml.Loader)
for obj in l:
    if type(obj) not in (MyOwn,Citation,Review):
        continue
    snip=None
    snip_year=None
    if 'journal' in obj:
        for try_year in range(obj['year'],obj['year']-3,-1):
            snip=get_snip(obj['journal'],try_year)
            if snip:
                snip_year=try_year
                break
    obj['snip']=snip
    obj['snip_year']=snip_year
    print('---')
    sys.stdout.write(yaml.dump(obj,allow_unicode=True,sort_keys=False,default_flow_style=None))

        


