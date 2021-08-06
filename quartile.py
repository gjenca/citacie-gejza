#!/usr/bin/env python3

import requests
import sys
import re
from bs4 import BeautifulSoup as BS
from bs4 import NavigableString
from collections import defaultdict
import difflib
import colorama
import time
import functools
colorama.init()

def isjunk(s):
    return not s.isalnum()

class Journal:

    def __init__(self,url,title):
        
        self.url=url
        self.title=title
        self.ratio=difflib.SequenceMatcher(isjunk,self.match_to.lower(),self.title.lower()).ratio()

    def __repr__(self):

        return f'{self.title} (ratio={self.ratio})'


def rows(tbody):

    tr=tbody.tr
    while tr:
        yield tr
        tr=tr.next_sibling

def cells(row):
    
    td=row.td
    while td:
        yield td
        td=td.next_sibling



URL='https://www.scimagojr.com/journalsearch.php'

@functools.lru_cache
def get_quartiles(search_string):

    journals=[]
    for page in range(1,6):
        params={
            'q':'+'.join(search_string.strip().split()),
            'page':page,
        }
        response=requests.get(URL,params)
        soup=BS(response.text,'html.parser')
        search_results=soup.find('div',class_='search_results').find_all('a')
        if len(search_results)==0:
            raise ValueError(f'"{search_string}": not found')
        if len(search_results)>2 and page==1:
            print(colorama.Fore.YELLOW+f'"{search_string}": Several journals found, going for the best match.'+colorama.Style.RESET_ALL,file=sys.stderr)
        Journal.match_to=search_string.strip()
        for a_element in search_results:
            path_to_journal=a_element['href']
            title=a_element.span.text.strip()
            journal_url=f'https://www.scimagojr.com/{path_to_journal}'
            journal=Journal(journal_url,title)
            journals.append(journal)
        paginator=re.search(r'\d+ - (\d+) of (\d+)',response.text)
        if paginator and paginator.group(1)==paginator.group(2):
            break
        time.sleep(0.1)
    journals=list(set(journals))
    journals.sort(key=lambda journal:journal.ratio,reverse=True)
    best=journals[0]
    if len(journals)>1:
        print(colorama.Fore.YELLOW+f'"{search_string}": found journal "{best.title}"'+colorama.Style.RESET_ALL,file=sys.stderr)
    response=requests.get(best.url)
    soup=BS(response.text,'html.parser')
    dashboard_tables=soup.find('div',class_='dashboard').find_all('table')
    quartiles_table=dashboard_tables[0]
    years=defaultdict(dict)
    if not quartiles_table.thead.find_all(string='Quartile'):
        print(colorama.Fore.RED+f'"{best.title}": No quartiles found!'+colorama.Style.RESET_ALL)
        raise ValueError
    for row in rows(quartiles_table.tbody):
        if type(row) is NavigableString:
            continue
        area,year,quartile=[cell.text for cell in cells(row)]
        years[year][area]=quartile
    ret={}
    for year in years:
        ret[int(year)]=min(years[year].values())
    return best.title,ret

if __name__=='__main__':
    if len(sys.argv)<2:
        print(get_quartiles('order'))
        print(get_quartiles('mathematica slovaca'))
    else:
        for journal in sys.argv[1:]:
            print(get_quartiles(journal))

