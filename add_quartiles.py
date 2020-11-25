#!/usr/bin/env python3
import yaml
import sys
from _yadata_types import MyOwn,Citation
from quartile import get_quartiles

l=yaml.load_all(sys.stdin,Loader=yaml.Loader)
for obj in l:
    obj['quartile']=None
    if 'journal' in obj:
        try:
            title,d=get_quartiles(obj['journal'])
        except ValueError:
            d={}
        if d:
            for try_year in range(obj['year'],obj['year']-3,-1):
                if  try_year in d:
                    obj['quartile']=d[try_year]
                    break
            else:
                obj['quartile']=None
        else:
            obj['quartile']=None
    else:
        obj['quartile']=None
    print('---')
    sys.stdout.write(yaml.dump(obj,allow_unicode=True,sort_keys=False,default_flow_style=None))

        


