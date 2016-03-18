#!/bin/sh

echo "Arrets des jeux precedents..."

./stop.sh $1

echo "Les anciens jeux ont été arreté. Lancement d'un nouveau jeu."

echo "Port du serveur : "
read port
echo "IP du serveur : "
read ip

python $1/client.py $ip $port > logs/client.log &

echo "Le serveur et les clients ont été lancé\nBon jeu !\nL'ip et le port utilisé sont ceux indiqué dans le fichier \"configuration.py\" "

