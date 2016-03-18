#!/bin/sh

if test $# -eq 0
then 
	echo "Syntaxe : $0 \`pwd\`"
	return 1
fi

echo "Arrets des jeux precedents..."

chmod +x $1/stop.sh >/dev/null
./stop.sh $1

echo "Les anciens jeux ont été arreté. Lancement d'un nouveau jeu."

echo "Port du serveur : "
read port
echo "IP du serveur : "
read ip

python $1/client.py $ip $port > $1/logs/client.log &

echo "Connexion au serveur de jeu...\nBon jeu !\nL'ip et le port utilisé sont ceux indiqué dans le fichier \"configuration.py\" "

