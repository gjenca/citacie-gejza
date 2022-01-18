%% if records_by_type("GrantRok")

### Granty
%% for grantrok in records_by_type("GrantRok")
 1. {{grantrok.grant.id}} -- fakultným účtovníctvom prešlo {{grantrok.vydavky}} EUR
%% endfor
%% endif
