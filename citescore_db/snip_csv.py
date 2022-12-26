
import shelve
import sys
import csv
import shelve
from make_key import make_key
    
d=shelve.open('snip.db')
if len(sys.argv)!=3:
    print(f'Usage: {sys.argv[0]} filename.csv year')
    sys.exit(1)
fnm=sys.argv[1]
year=sys.argv[2]
with open(fnm) as f:
    csvreader=csv.reader(f)
    for row in csvreader:
        journal=row[1]
        print(make_key(journal,year))



