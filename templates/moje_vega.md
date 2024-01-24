
%% for rec in records_by_type("MyOwn") | sort_by('year.year')
 1. {{ rec.authors_format("{f. }{vv}{ll{ }}{, jj}")|join(", ") }}: {{rec.title}}, {{rec.journal}}.  {{rec.volume}} ({{rec.year}}), {{rec.startpage}}-{{rec.endpage}}; {{ rec.citedby | length }} citácií
%% endfor


