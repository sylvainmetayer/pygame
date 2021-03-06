#!/usr/bin/python2
# -*- coding: utf-8 -*-

BALL_SPEED = 3
NB_VIE_BRIQUE_0 = 3
ALLOW_SOUND = True
PORT = 8888
ETH = "wlan0"
FREQUENCE_TIR = 150

"""
Configuration personnalisable :
    - BALL_SPEED : Entier seulement. Détermine la vitesse de la balle. Recommandé entre 2 et 4.
    - NB_VIE_BRIQUE_0 : Nombre de fois qu'il faut toucher une brique pour la casser. Entier seulement
    - ALLOW_SOUND = True/False. Permet de couper/activer le son.
    Si jamais on lance le fichier python sans paramètres, les fichiers seront chargés avec les valeurs PORT et ETH
    - ETH : Interface réseau à utiliser pour récupérer l'adresse IP
    - PORT : Port du jeu.
    - FREQUENCE_TIR : La fréquence de tir des joueurs.
"""
