
import find_journal
import requests
from bs4 import BeautifulSoup as BS
from bs4 import NavigableString

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

def sjr(search):

    name,url=find_journal.best_match_url(search)
    response=requests.get(url)
    soup=BS(response.text,'html.parser')
    dashboards=soup.find_all('div',class_='dashboard')
    sjr_table=dashboards[1].find('table')
    years={}
    for row in rows(sjr_table.tbody):
        if type(row) is NavigableString:
            continue
        year,value=[cell.text for cell in cells(row)]
        years[year]=value

    return years
    
if __name__=='__main__':

    print(sjr('mathematica slovaca'))


