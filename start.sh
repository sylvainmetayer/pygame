#!/bin/sh

echo "Usage : $0 `pwd`"

python $1/serveur.py > logs/serveur.log &
sleep 3 #pour être sur que le serveur soit lancé
python $1/client.py > logs/client1.log &
python $1/client.py > logs/client2.log &

echo "Le serveur et les clients ont été lancé"

