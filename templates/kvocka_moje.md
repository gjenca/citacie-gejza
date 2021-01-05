%% import "macros.jinja" as macros
%% if records_by_type("MyOwn")
### {{ extra.title }}
%% for rec in records_by_type("MyOwn")
 1. {{ macros.publication(rec) }}
%% endfor
%% endif
