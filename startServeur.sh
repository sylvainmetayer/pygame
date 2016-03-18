#!/bin/sh

if test $# -eq 0
then
        echo "Syntaxe : $0 \`pwd\`"
        return 1
else

        echo "Arrets des jeux precedents..."

        ./stop.sh $1

	echo "Les anciens jeux ont été arreté. Lancement d'un nouveau jeu."

	python $1/serveur.py | tee logs/serveur.log &
        sleep 1 #pour être sur que le serveur soit lancé
	python $1/client.py > logs/client.log &

        echo "Le serveur et les clients ont été lancé\nBon jeu !\nL'ip et le port utilisé sont ceux indiqué dans le fichier \"configuration.py\" "
fi