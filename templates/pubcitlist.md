%% set count = namespace(myown=0,citwos=0,citscopus=0,cit=0)
%% macro publication(rec)
{{  rec.authors_format("{f. }{vv}{ll{ }}{, jj}")|join(", ") }}: {{rec.title}},
%% if rec.type=='article'
  *{{rec.journal}}*,
**{{rec.volume}}**
({{rec.year}}),
%% elif rec.type=='inproceedings' or rec.type=='incollection'
In: *{{rec.booktitle}}*,
       %% if rec.series:
{{rec.series}},
           %% if rec.volume: 
Vol. **{{rec.volume}}**,
           %% endif 
       %% endif
       %% if rec.publisher: 
{{rec.publisher}},
       %% endif    
{{rec.year}},
    %% endif
    %% if rec.startpage and rec.endpage
{{rec.startpage}}-{{rec.endpage}},
    %% endif
    %% if rec.article_number
art. nr. {{rec.article_number}},
    %% endif
%% endmacro
%% for rec in records_by_type('MyOwn')
  %% if rec.citedby:
<p>

### Paper:  
%% set count.myown = count.myown + 1
  {{ publication(rec) }}
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
 1. {{ publication(rec_cited) | join }}{% for tag in rec_cited.tags %}[{{tag}}] {% endfor %}
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

