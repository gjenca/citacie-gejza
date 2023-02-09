%% import "macros.jinja" as macros
%% if records_by_type("Citation")

### {{ extra.title }}
%% for rec in records_by_type("MyOwn") | sort_by('year')
%% if rec.citedby:

#### Článok: 
<p>
{{macros.publication(rec)}}
<p>
#### Citovaný v ({{ rec.citedby | length}}):
%% for rec_cited in rec.citedby | sort_by('year')
 1. {{macros.publication(rec_cited)}}
%% endfor
%% endif
%% endfor
%% endif
