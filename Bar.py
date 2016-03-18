#!/usr/bin/python2
# -*- coding: utf-8 -*-

import pygame.sprite

from PodSixNet.Connection import ConnectionListener

import outils


# Partie Serveur

class Bar(pygame.sprite.Sprite):
    """
    Classe représentant la barre d'un joueur, côté serveur.
    Attribut : une image, une position (le rect de l'image) et une vitesse.
    """

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image, self.rect = outils.Fonction.load_png('images/bar.png')

        # Position de départ
        self.rect.center = [outils.SCREEN_WIDTH / 2, outils.SCREEN_HEIGHT / 2]

        self.speed = [3, 3]
        self.pas = 10  # Vitesse de déplacement

    def left(self):
        if self.rect.left <= -200:
            self.rect = self.rect.move([0, 0])
        else:
            self.rect = self.rect.move([-self.pas, 0])

    def right(self):
        if self.rect.right >= outils.SCREEN_WIDTH + 200:
            self.rect = self.rect.move([0, 0])
        else:
            self.rect = self.rect.move([self.pas, 0])

    def update(self):

        # On gère que la vitesse ne soit pas trop élevée.
        if self.speed[0] >= 5 or self.speed[0] >= -5:
            self.speed[0] = 0
        if self.speed[1] >= 5 or self.speed[1] >= -5:
            self.speed[1] = 0

        self.rect = self.rect.move(self.speed)

    def set_position(self, position):
        """
        Cette fonction permet de définir la position de départ. Elle est normalement uniquement utilisée
        lors de l'instanciation de joueurs
        :param position: tuple de la position
        """
        self.rect.center = position


class Bars(pygame.sprite.RenderClear):
    """
    Classe qui contient un tableau de clients de bar
    """

    def __init__(self):
        pygame.sprite.Group.__init__(self)

    def update(self):
        for client in self.sprites():
            client.bar.update()

    def __getitem__(self, item):
        for key, value in enumerate(self.sprites()):
            if key == item:
                return value


# PARTIE CLIENT

class BarClient(pygame.sprite.Sprite):
    '''
    Classe représentant la bar sur laquelle la balle rebondit
    '''

    def __init__(self, center=(outils.SCREEN_WIDTH / 2, outils.SCREEN_HEIGHT / 2)):
        pygame.sprite.Sprite.__init__(self)
        self.image, self.rect = outils.Fonction.load_png('images/bar.png')
        self.rect.center = center
        self.speed = [3, 3]
        self.pas = 10

    def update(self):
        pass

class BarsClient(pygame.sprite.Group, ConnectionListener):
    """
    Classe de groupe de tirs côté client.
    """

    def __init__(self):
        pygame.sprite.Group.__init__(self)

    def update(self):
        self.Pump()

    def Network_bar(self, data):
        self.empty()
        donnees = data["liste"]
        for xy in donnees:
            bar = BarClient(xy)
            self.add(bar)
