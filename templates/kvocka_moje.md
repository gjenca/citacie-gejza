%% import "macros.jinja" as macros
%% if records_by_type("MyOwn")
### {{ extra.title }}
%% for rec in records_by_type("MyOwn") | sort_by('year')
 1. {{ macros.publication(rec) }}
%% endfor
%% endif
