#!/usr/bin/python2
# -*- coding: utf-8 -*-

# Ce fichier contient toutes les variables utilisées dans le jeu.

import functions

SCREEN_WIDTH = 1024
SCREEN_HEIGHT = 768

POS_J1 = [SCREEN_WIDTH /2, SCREEN_HEIGHT / 3]
POS_J2 = [SCREEN_WIDTH /2, SCREEN_HEIGHT - 150]


"""
 Configuration par défaut :
    Port 8888
    On récupère l'adresse IP de l'interface ETH (à définir)
"""

PORT = 8888
ETH = "wlan0"

IP = functions.Fonction.get_ip_address(ETH)
