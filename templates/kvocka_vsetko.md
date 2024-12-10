%% import "macros.jinja" as macros
## Publikácie

%% for rec in records_by_type('MyOwn') | sort_by('year.year')
 1. {{ macros.publication(rec) }}
%% endfor
