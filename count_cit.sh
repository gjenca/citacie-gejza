#!/bin/bash
if [ "$1" == "" ]
then
   FILT=True
else
   FILT="$1"
fi
yadata read pubcit ! filter "$FILT" ! type Citation ! exec -n 'print(cites)' |
	tr ',' '\n' | wc -l

