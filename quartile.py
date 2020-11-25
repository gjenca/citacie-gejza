#!/usr/bin/env python3

import requests
import sys
from bs4 import BeautifulSoup as BS
from bs4 import NavigableString
from collections import defaultdict
import difflib
import colorama
colorama.init()

def isjunk(s):
    return s.isspace()

class Journal:

    def __init__(self,url,title):
        
        self.url=url
        self.title=title
        self.ratio=difflib.SequenceMatcher(isjunk,self.match_to.lower(),self.title).ratio()

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
if len(sys.argv)!=2:
    print(f'Usage: {sys.argv[0]} journal_name',file=sys.stderr)
    sys.exit(1)

params={'q':'+'.join(sys.argv[1].strip().split())}
response=requests.get(URL,params)
soup=BS(response.text,'html.parser')
search_results=soup.find('div',class_='search_results').find_all('a')
if len(search_results)==0:
    print(colorama.Fore.RED+'Journal not found.'+colorama.Style.RESET_ALL,file=sys.stderr)
    sys.exit(2)
if len(search_results)>2:
    print(colorama.Fore.YELLOW+'Several journals found, going for the best match. Maybe try a more specific query'+colorama.Style.RESET_ALL)
journals=[]
Journal.match_to=sys.argv[1].strip()
for a_element in search_results:
    path_to_journal=a_element['href']
    title=a_element.span.text.strip()
    journal_url=f'https://www.scimagojr.com/{path_to_journal}'
#    response=requests.get(journal_url)
#    soup=BS(response.text,'html.parser')
    journal=Journal(journal_url,title)
    journals.append(journal)
journals.sort(key=lambda journal:journal.ratio,reverse=True)
best=journals[0]
response=requests.get(best.url)
print(f'Journal: {best.title}')
soup=BS(response.text,'html.parser')
dashboard_tables=soup.find('div',class_='dashboard').find_all('table')
quartiles_table=dashboard_tables[0]
years=defaultdict(dict)
if not quartiles_table.thead.find_all(string='Quartile'):
    print(colorama.Fore.RED+'No quartiles found!'+colorama.Style.RESET_ALL)
    exit(1)
for row in rows(quartiles_table.tbody):
    if type(row) is NavigableString:
        continue
    area,year,quartile=[cell.text for cell in cells(row)]
    years[year][area]=quartile
for year in years:
    print(year,max(years[year].values()))



