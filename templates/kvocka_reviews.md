%% if records_by_type("Review")
### Posudok časopiseckého článku WoS, SCOPUS
%% for review in records_by_type("Review")
 1. {{review.journal}} {{review.id}} 
%% endfor
%% endif
