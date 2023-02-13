%% import "macros.jinja" as macros
%% set count = namespace(myown=0,citwos=0,citscopus=0,cit=0)
%% set wos = record_by_tag_and_key('!Tag','wos')
%% set scopus = record_by_tag_and_key('!Tag','scopus')
%% for rec in records_by_type('MyOwn') | sort_by('year')
  %% if rec.citedby:
<p>

### Paper:  
%% set count.myown = count.myown + 1
  {{ macros.publication(rec) }}
    %% if rec.preprint
arxiv:{{rec.preprint}},
    %% endif      
<p>  
### Cited in ({{ rec.citedby | length}}):
  %% for rec_cited in rec.citedby | sort_by('year')
    %% set count.cit = count.cit +1
 1. {{ macros.publication(rec_cited) | join }}{% for tag in rec_cited.tags %}[{{tag}}] {% endfor %}
    %% if 'as-preprint' in edge_tags[("cites",rec_cited._key,rec._key)]:
(Cited as preprint)
    %% endif
  %% endfor
  %%endif
%% endfor
<p>

### Number of cited papers: {{count.myown}}
### Number of citations: {{count.cit}}
### Number of citations in WOS: {{wos.number_of_citations}}
### Number of citations in Scopus: {{scopus.number_of_citations}}

