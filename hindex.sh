#!/bin/bash
if [ "$1" == "" ]
then
   FILT=True
else
   FILT="$1"
fi
yadata read pubcit ! filter "$FILT" ! render timescited.txt | sort -rn | cat -n |
while read n x
do
	if [ $n -le $x ]
	then
		echo 1
	fi
done | wc -l


