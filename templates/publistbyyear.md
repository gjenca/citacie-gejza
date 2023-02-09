%% import "macros.jinja" as macros
%% for year in records_by_type('Year') | sort_by('year')
## {{year.year}}
%% for myown in year.myowns:
 1. {{ macros.publication(myown) | join }}
%% endfor
%% endfor

