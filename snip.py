#!/usr/bin/env python3

from pyxlsb import open_workbook
import glob
import re


def get_snip(journal,year):

    fnm=glob.glob('citescore_xls/*xls*')[0]
    book=open_workbook(fnm)
    snips=[]
    with book.get_sheet(f'CiteScore {year}') as sheet:
        for i,row in enumerate(sheet.rows()):
            if row[1].v.strip().lower()==journal.strip().lower():
                snip=row[6].v
                snips.append(snip)
    return max(snips)

if __name__=='__main__':
    print('Mathematica Slovaca SNIP for 2019')
    print(get_snip('Mathematica Slovaca',2019))



