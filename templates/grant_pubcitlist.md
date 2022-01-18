%% import "macros.jinja" as macros
%% set count = namespace(myown=0,citwos=0,citscopus=0,cit=0)
%% set grant = records_by_type('Grant')[0]
%% for rec in grant.myowns:
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
  %% for rec_cited in rec.citedby:
    %% set count.cit = count.cit +1
    %% if "wos" in rec_cited.tags
      %% set count.citwos = count.citwos +1
    %% endif
    %% if "scopus" in rec_cited.tags
      %% set count.citscopus = count.citscopus +1
    %% endif
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
### Number of citations in WOS: {{count.citwos}}
### Number of citations in Scopus: {{count.citscopus}}

