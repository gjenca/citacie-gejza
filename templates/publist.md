%% import "macros.jinja" as macros
%% for rec in records_by_type('MyOwn') | sort_by('year')
 1. {{ macros.publication(rec) | join }}
%% endfor

