#!/usr/bin/env python3

from pyxlsb import open_workbook
import sys
import re
import shelve

def make_key(journal,year):

    journal_key=''.join(c.lower() for c in journal if c.isalpha())
    return f'{year}{journal_key}'


if __name__=='__main__':
    
    d=shelve.open('snip.db')
    book=open_workbook(sys.argv[1])
    for sheetname in book.sheets:
        m=re.match(r'CiteScore (\d+)',sheetname)
        if not m:
            continue
        year=m.group(1)
        print('Year:',year)
        with book.get_sheet(sheetname) as sheet:
            for i,row in enumerate(sheet.rows()):
                if i and not (i%1000):
                    print(i)
                journal=row[1].v
                snip=row[6].v
                d[make_key(journal,year)]=snip
    d.close()



