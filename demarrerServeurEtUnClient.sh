#!/bin/sh

echo "Arrets des jeux precedents..."

./stop.sh $1

echo "Les precedents jeux ont ete arretes.\nLancement d'un nouveau jeu."

python $1/serveur.py | tee logs/serveur.log &
sleep 1 #pour être sur que le serveur soit lancé
python $1/client.py > logs/client2.log &

echo "Le serveur et un client ont été lancé\nMerci de lancer un deuxième client sur un autre poste"

