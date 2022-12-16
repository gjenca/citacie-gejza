#!/usr/bin/env python3

import shelve
from citescore_db.make_key import make_key

def get_snip(journal,year):

    d=shelve.open('citescore_db/snip.db')
    key=make_key(journal,year)
    if key in d:
        return d[make_key(journal,year)]

if __name__=='__main__':
    for journal in (
        'journal of combinatorial theory series a',
        'Fuzzy Sets and Systems',
    ):
        print(journal,':')
        for year in range(2011,2020):
            snip=get_snip(journal,year)
            print(f'{year}: {snip}')



