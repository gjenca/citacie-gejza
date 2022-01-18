%% import "macros.jinja" as macros
%% for grant in records_by_type('Grant')
## Grant:{{grant.id}}
%% for myown in grant.myowns:
 1. {{ macros.publication(myown) | join }}
%% endfor
%% endfor

