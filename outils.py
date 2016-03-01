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
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        return socket.inet_ntoa(fcntl.ioctl(
            s.fileno(),
            0x8915,  # SIOCGIFADDR
            struct.pack('256s', ifname[:15])
        )[20:24])

SCREEN_WIDTH = 1024
SCREEN_HEIGHT = 768

SIZE_SERVEUR = ((SCREEN_WIDTH / 4, SCREEN_HEIGHT / 4))

POS_J1 = [SCREEN_WIDTH /2, SCREEN_HEIGHT / 3]
POS_J2 = [SCREEN_WIDTH /2, SCREEN_HEIGHT - 150]
POS_BALLE = [SCREEN_WIDTH /2, SCREEN_HEIGHT / 2]

"""
 Configuration par défaut :
    Port 8888
    On récupère l'adresse IP de l'interface ETH (à préciser et adapter)
"""

PORT = 8888
ETH = "wlan0"

IP = Fonction.get_ip_address(ETH)
