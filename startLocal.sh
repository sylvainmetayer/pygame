#!/bin/sh

if test $# -eq 0
then
	echo "Syntaxe : $0 \`pwd\`"
	return 1
else

	echo "Arrets des jeux precedents..."

	./stop.sh $1

	echo "Les precedents jeux ont ete arretes.\nLancement d'un nouveau jeu."


	python $1/serveur.py 127.0.0.1 8888 > logs/serveur_lo.log &
	sleep 1 #pour être sur que le serveur soit lancé
	python $1/client.py 127.0.0.1 8888 > logs/client1_lo.log &
	python $1/client.py 127.0.0.1 8888 > logs/client2_lo.log &

	echo "Le serveur et les clients ont été lancé\nBon jeu !"
fi
