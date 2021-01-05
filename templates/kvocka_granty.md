%% if records_by_type("Grant")

<p>
### Granty
%% for grant in records_by_type("Grant")
 1. {{grant.id}} -- fakultným účtovníctvom prešlo {{grant.vydavky}} EUR
%% endfor
%% endif
