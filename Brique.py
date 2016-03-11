#!/usr/bin/python2
# -*- coding: utf-8 -*-

import pygame.sprite
import outils


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
        if self.rect.colliderect(balle.rect):
            self.hit()
            if self.rect.center[0] >= balle.rect.center[0] and self.rect.center[1] <= balle.rect.center[1] :
                # Coté gauche
                if balle.speed == outils.RIGHT_UP:
                    balle.deplacement(outils.LEFT_UP)
                else:
                    balle.deplacement(outils.LEFT_DOWN)
            elif self.rect.center[1] >= balle.rect.center[1] and self.rect.center[0] <= balle.rect.center[0]:
                # Côté droit
                if balle.speed == outils.LEFT_UP:
                    balle.deplacement(outils.RIGHT_UP)
                else:
                    balle.deplacement(outils.RIGHT_DOWN)
            elif self.rect.center[0] <= balle.rect.center[0] and self.rect.center[1] <= balle.rect.center[1]:
                # Cote haut
                if balle.speed == outils.RIGHT_DOWN:
                    balle.deplacement(outils.RIGHT_UP)
                else:
                    balle.deplacement(outils.LEFT_UP)
            elif self.rect.center[0] >= balle.rect.center[0] and self.rect.center[1] >= balle.rect.center[1]:
                # Cote bas
                if balle.speed == outils.RIGHT_UP:
                    balle.deplacement(outils.RIGHT_DOWN)
                else:
                    balle.deplacement(outils.LEFT_DOWN)
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
