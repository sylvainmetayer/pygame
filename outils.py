#!/usr/bin/python2
# -*- coding: utf-8 -*-

# Ce fichier contient toutes les variables utilisées dans le jeu.

import fcntl
import socket
import struct


class Fonction():
    def __init__(self):
        pass

    @staticmethod
    def get_ip_address(ifname):
        """
        Cette fonction retourne l'adresse IP selon l'interface donnée (wlan0, eth0, ...)
        """
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        return socket.inet_ntoa(fcntl.ioctl(
            s.fileno(),
            0x8915,  # SIOCGIFADDR
            struct.pack('256s', ifname[:15])
        )[20:24])


SCREEN_WIDTH = 1024
SCREEN_HEIGHT = 768

SIZE_SERVEUR = ((SCREEN_WIDTH / 4, SCREEN_HEIGHT / 4))

POS_J1 = [SCREEN_WIDTH / 2, SCREEN_HEIGHT / 3]
POS_J2 = [SCREEN_WIDTH / 2, SCREEN_HEIGHT - 150]

J1 = 0
J2 = 1
BALL_SPEED = 3

# DEPLACEMENT BALLE
DOWN = [0, BALL_SPEED]
UP = [0, -BALL_SPEED]
LEFT_UP = [BALL_SPEED, -BALL_SPEED]
LEFT_DOWN = [BALL_SPEED, BALL_SPEED]
RIGHT_DOWN = [-BALL_SPEED, BALL_SPEED]
RIGHT_UP = [-BALL_SPEED, -BALL_SPEED]

POS_BALLE = [SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2]

"""
 Configuration par défaut (utilisation locale) :
    Port 8888
    On récupère l'adresse IP de l'interface ETH (à préciser et adapter)
"""

PORT = 8888
ETH = "wlan0"
IP = Fonction.get_ip_address(ETH)
