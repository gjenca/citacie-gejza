
import shelve
import sys
import xlrd
from make_key import make_key

if lens(sys.argv!=3) 
    print(f'Usage: {sys.argv[0]} filrname year')
    sys.exit(1)
fnm=sys.argv[1]
year=sys.argv[2]
book=xldr.open_workbook(fnm)
sheet=book.sheet_by_index(0)
for r in range(1,sheet.nrows):
    print(sheet.cell_value(r,1))



