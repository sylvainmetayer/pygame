#!/usr/bin/python2
# -*- coding: utf-8 -*-

import pygame.sprite

from PodSixNet.Connection import ConnectionListener

import outils


class Tir(pygame.sprite.Sprite):
    """
    Classe de tir du vaisseau
    """

    def __init__(self, bar):
        pygame.sprite.Sprite.__init__(self)
        self.image, self.rect = outils.Fonction.load_png('images/shot.png')
        self.speed = [0, -1]
        self.rect.center = bar.rect.center

    def update(self):
        """

        :return: True si le tir est mort, False sinon
        """
        self.rect = self.rect.move([0, -10])
        if self.rect.top <= -20:
            self.kill()
            return True
        return False


class Tirs(pygame.sprite.Group):
    """
    Classe le groupe de tirs côté serveur.
    """

    def __init__(self):
        pygame.sprite.Group.__init__(self)

    def update(self):
        for tir in self.sprites():
            retour = tir.update()
            if retour == True:
                self.remove(tir);  # Le tir est mort.


class TirClient(pygame.sprite.Sprite):
    """
    Classe de tir
    """

    def __init__(self, coordonnees):
        pygame.sprite.Sprite.__init__(self)
        self.image, self.rect = outils.Fonction.load_png("images/shot.png");
        self.speed = [0, -1]
        self.rect.center = coordonnees

    def update(self):
        pass


class TirsClient(pygame.sprite.Group, ConnectionListener):
    """
    Classe de groupe de tirs côté client.
    """

    def __init__(self):
        pygame.sprite.Group.__init__(self)

    def update(self):
        self.Pump()

    def Network_shot(self, data):
        self.empty()
        listeTir = data["liste"]
        print listeTir
        print "LEL"
        for xy in listeTir:
            tir = TirClient(xy)
            self.add(tir)
