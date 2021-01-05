%% import "macros.jinja" as macros
%% for rec in records_by_type('MyOwn')
 1. {{ macros.publication(rec) | join }}
%% endfor

