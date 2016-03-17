#!/usr/bin/python2
# -*- coding: utf-8 -*-

import pygame.sprite

from PodSixNet.Connection import ConnectionListener

import outils


# PARTIE SERVEUR

class Brique(pygame.sprite.Sprite):
    """
    Classe qui réprésente une brique normale
    Cette classe à 2 vies.
    """

    def __init__(self, position):
        pygame.sprite.Sprite.__init__(self)
        self.image, self.rect = outils.Fonction.load_png("images/brique_0.png")
        self.rect.center = position
        self.vie = outils.NB_VIE_BRIQUE_0

    def hit(self):
        self.vie -= 1
        if self.vie == 0:
            self.kill()

    def gestion(self, balle):
        width_brique = (self.rect.center[0] - self.rect.left) + (self.rect.center[0] - self.rect.right )

        if pygame.sprite.collide_circle(self, balle):
            self.hit()
            if self.rect.center[0] > balle.rect.center[0] and self.rect.center[1] < balle.rect.center[1] :
                print "Recentrer balle à gauche de la brique"

                #balle.rect.right = self.rect.left - 2
                # Coté gauche
                if balle.speed == outils.RIGHT_UP:
                    balle.deplacement(outils.LEFT_UP)
                else:
                    balle.deplacement(outils.LEFT_DOWN)
            elif self.rect.center[1] > balle.rect.center[1] and self.rect.center[0] < balle.rect.center[0]:
                # Côté droit
                print "Recentrer balle à droite de la brique"
                #balle.rect.left = self.rect.right + 2
                if balle.speed == outils.LEFT_UP:
                    balle.deplacement(outils.RIGHT_UP)
                else:
                    balle.deplacement(outils.RIGHT_DOWN)
            elif self.rect.center[0] < balle.rect.center[0] and self.rect.center[1] < balle.rect.center[1]:
                # Cote haut
                print "Recentrer balle en bas de la brique"
                #balle.rect.bottom = self.rect.top - 2
                balle.reverseDirection()
                if (balle.speed == outils.RIGHT_DOWN and balle.direction == outils.BAS) :
                    balle.deplacement(outils.RIGHT_UP)
                elif balle.speed == outils.LEFT_DOWN and balle.direction == outils.BAS:
                    balle.deplacement(outils.LEFT_UP)
                else:
                    balle.deplacement(outils.DOWN)
            elif self.rect.center[0] > balle.rect.center[0] and self.rect.center[1] > balle.rect.center[1]:
                # Cote bas
                balle.reverseDirection()
                print "Recentrer balle en haut de la brique"
                #balle.rect.top = self.rect.bottom + 2
                if (balle.speed == outils.RIGHT_UP and balle.direction == outils.HAUT) :
                    balle.deplacement(outils.RIGHT_DOWN)
                elif balle.speed == outils.LEFT_UP and balle.direction == outils.HAUT:
                    balle.deplacement(outils.LEFT_DOWN)
                else:
                    balle.deplacement(outils.UP)
            return True
        return False

class Briques(pygame.sprite.RenderClear):
    """
    Classe qui contient un tableau de briques
    """

    def __init__(self):
        pygame.sprite.Group.__init__(self)

    def __getitem__(self, item):
        for key, value in enumerate(self.sprites()):
            if key == item:
                return value
    def gestion(self, balle):
        for brique in self.sprites():
            hit = brique.gestion(balle)
            if hit:
                return True

        return False

# PARTIE CLIENT

class BriqueClient(pygame.sprite.Sprite):
    """
    Classe qui réprésente une brique normale
    Cette classe à 2 vies.
    """

    def __init__(self, position):
        pygame.sprite.Sprite.__init__(self)
        self.image, self.rect = outils.Fonction.load_png("images/brique_0.png")
        self.rect.center = position

    def update(self):
        pass


class BriquesClient(pygame.sprite.RenderClear, ConnectionListener):
    """
    Classe qui contient un tableau de briques
    """

    def __init__(self):
        pygame.sprite.Group.__init__(self)

    def __getitem__(self, item):
        for key, value in enumerate(self.sprites()):
            if key == item:
                return value

    def update(self):
        self.Pump()

    def Network_briques(self, data):
        self.empty()
        donnees = data["liste"]
        for xy in donnees:
            brique = BriqueClient(xy)
            self.add(brique)
