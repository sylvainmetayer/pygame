#!/bin/sh

echo "Arrets des jeux precedents..."
# On s'assure de ne kill que les process correspondant au pwd passé,
# afin de ne pas interferer avec les autres process python

kill -9 `ps -aux | grep "python $1" | tr -s " " | cut -d" " -f2`1>/dev/null 2>&1
kill -9 `ps -aux | grep "python $1" | tr -s " " | cut -d" " -f2`1>/dev/null 2>&1
kill -9 `ps -aux | grep "python $1" | tr -s " " | cut -d" " -f2`1>/dev/null 2>&1

echo "Les precedents jeux ont ete arretes.\nLancement d'un nouveau jeu."

python $1/serveur.py > logs/serveur.log &
sleep 1 #pour être sur que le serveur soit lancé
python $1/client.py > logs/client1.log &
python $1/client.py > logs/client2.log &

echo "Le serveur et les clients ont été lancé\n"
