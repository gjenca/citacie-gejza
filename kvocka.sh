#!/bin/bash
if [ $# != 1 ] ; then
echo 'Usage: ./kvocka.sh YEAR'
exit 1
fi
YEAR=$1
VOCTAG=voc${YEAR}
let PASTYEAR=YEAR-1
let NEXTYEAR=YEAR+1
echo '# VOC '$YEAR 
yadata read pubcit ! type MyOwn ! filter "'${VOCTAG}' in tags" ! sort -k year > voc${YEAR}.myown.yaml
yadata filter '"cc" in tags' < voc${YEAR}.myown.yaml | 
	yadata render -p '%%' -e '{ title: "Karentované (Current Contents) časopisy zahraničné aj domáce" }' kvocka_moje.md
yadata filter '"scopus" in tags and "cc" not in tags' < voc${YEAR}.myown.yaml | 
	yadata render -p '%%' -e '{ title: "Časopisy zahraničné aj domáce evidované v databáze SCOPUS" }' kvocka_moje.md
yadata read pubcit ! type MyOwn Citation ! filter -t Citation "'${VOCTAG}' in tags" ! exec 'is_old = (year == '${PASTYEAR}' and "'${VOCTAG}'" in tags)' ! sort -k year > voc${YEAR}.yaml
yadata filter -t Citation '("wos" in tags or "sci" in tags or "scopus" in tags) and not "dautor" in tags' < voc${YEAR}.yaml |
	yadata render -p '%%' -e '{ title: "Citácie podľa SCI, multidisciplinárne ISI, SCOPUS – len zahraničný autor" }' kvocka_citacie.md
yadata filter -t Citation '("wos" in tags or "sci" in tags or "scopus" in tags) and "dautor" in tags' < voc${YEAR}.yaml |
	yadata render -p '%%' -e '{ title: "Citácie podľa SCI, multidisciplinárne ISI, SCOPUS – domáci autor" }' kvocka_citacie.md
yadata read pubcit ! type Review ! filter "'${VOCTAG}' in tags" ! filter '"wos" in tags or "scopus" in tags' ! render -p '%%' kvocka_reviews.md
yadata read pubcit ! type Grant ! filter "year==${YEAR}" ! render -p '%%' kvocka_granty.md
#rm voc${YEAR}.myown.yaml
#rm voc${YEAR}.yaml

