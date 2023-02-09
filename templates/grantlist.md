%% import "macros.jinja" as macros
%% for grant in records_by_type('Grant') | sort_by('id')
## Grant:{{grant.id}}
%% for myown in grant.myowns | sort_by('year')
 1. {{ macros.publication(myown) | join }}
%% endfor
%% endfor

