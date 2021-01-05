%% import "macros.jinja" as macros
%% if records_by_type("Citation")

### {{ extra.title }}
%% for rec in records_by_type("MyOwn")
%% if rec.citedby:

#### Článok: 
<p>
{{macros.publication(rec)}}
<p>
#### Citovaný v ({{ rec.citedby | length}}):
%% for rec_cited in rec.citedby:
 1. {{macros.publication(rec_cited)}}
%% endfor
%% endif
%% endfor
%% endif
