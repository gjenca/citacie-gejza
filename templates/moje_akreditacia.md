# doc. Mgr. Gejza Jenča PhD

%% for rec in records_by_type("MyOwn"):
 1. {{ rec.authors_format("{f. }{vv}{ll{ }}{, jj}")|join(", ") }}: {{rec.title}} In {{rec.journal}}.  Vol. {{rec.volume}}, ({{rec.year}}) s.{{rec.startpage}}-{{rec.endpage}} ({{rec.quartile}} - SJR {{rec.quartile_year}}, {{rec.snip}} - SJR SNIP {{rec.snip_year}})
   Počet citácií: {{ rec.citedby | length }}
%% endfor


