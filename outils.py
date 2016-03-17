#!/usr/bin/python2
# -*- coding: utf-8 -*-

# Ce fichier contient toutes les variables utilisées dans le jeu.

import fcntl
import os
import pygame
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

    @staticmethod
    def load_png(name):
        """
        Permet de charger une image, via son nom.
        :param name: le chemin de l'image à charger.
        :return: l'image et le rectangle associé à l'image.
        """
        fullname = os.path.join('.', name)
        try:
            image = pygame.image.load(fullname)
            if image.get_alpha is None:
                image = image.convert()
            else:
                image = image.convert_alpha()
        except pygame.error, message:
            print 'Cannot load image:', fullname
            raise SystemExit, message
        return image, image.get_rect()



# Definitions des côtés de jeu
SCREEN_WIDTH = 1024
SCREEN_HEIGHT = 768
COTE_GAUCHE = 0
COTE_DROIT = SCREEN_WIDTH
COTE_HAUT = 0
COTE_BAS = SCREEN_HEIGHT


SIZE_SERVEUR = ((SCREEN_WIDTH / 4, SCREEN_HEIGHT / 4))

POS_J1 = [SCREEN_WIDTH / 2, SCREEN_HEIGHT / 3 - 100]
POS_J2 = [SCREEN_WIDTH / 2, SCREEN_HEIGHT - 100]

KILL_J1 = 10;
KILL_J2 = 20;

J1 = 0
J2 = 1
BALL_SPEED = 3
MARGE_ZONE = 99

#Gestion pour les murs
HAUT = 1
BAS = 0

# DEPLACEMENT BALLE
DOWN = [0, BALL_SPEED]
UP = [0, -BALL_SPEED]
LEFT_UP = [-BALL_SPEED, -BALL_SPEED]
LEFT_DOWN = [-BALL_SPEED, BALL_SPEED]
RIGHT_DOWN = [BALL_SPEED, BALL_SPEED]
RIGHT_UP = [BALL_SPEED, -BALL_SPEED]

POS_BALLE = [SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2]

PLAY_SOUND = 111
# LEs briques
NB_VIE_BRIQUE_0 = 2

"""
 Configuration par défaut (utilisation locale) :
    Port 8888
    On récupère l'adresse IP de l'interface ETH (à préciser et adapter)
"""

PORT = 8888
ETH = "wlan0"
IP = Fonction.get_ip_address(ETH)
