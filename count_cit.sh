#!/bin/bash
if [ "$1" == "" ]
then
   FILT=True
else
   FILT="$1"
fi
yadata read pubcit ! type Citation ! filter "$FILT" ! exec -n 'print(cites)' |
	tr ',' '\n' | wc -l

