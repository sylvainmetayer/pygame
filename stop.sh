#!/bin/sh

ps -a| grep python |cut -d" " -f1 > tmp

while IFS='' read -r line || [[ -n "$line" ]]; do
    kill -9 $line 
done < tmp
rm tmp
