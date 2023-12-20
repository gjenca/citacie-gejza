#!/bin/bash
GRANT="$1"
YEAR="$2"
cat << END
# $GRANT roky $YEAR--súčasnosť
END

yadata read pubcit ! filter -t MyOwn 'year>='"$YEAR" ! filter -t MyOwn '"'$GRANT'" in grants' ! sort -t MyOwn -k year > grant.myown.yaml
yadata render -s -e '{title: Publikované články}' kvocka_moje.md < grant.myown.yaml
yadata read pubcit ! filter -t Citation 'year >= '"$YEAR" ! filter -t MyOwn '"'$GRANT'" in grants' ! sort -t Citation -k year > grant.yaml
	yadata render -s -e '{title: Citácie}' kvocka_citacie.md < grant.yaml
