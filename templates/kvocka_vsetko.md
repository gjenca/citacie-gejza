%% import "macros.jinja" as macros
%% set tag = records_by_type("Tag")[0]
# {{tag.tag}}
## Publikácie

%% for rec in tag.myowns:
 1. {{ macros.publication(rec) }}
%% endfor
