#!/usr/bin/python2
# -*- coding: utf-8 -*-

import pygame.sprite
import outils

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
        if self.rect.left <= 0:
            self.rect = self.rect.move([0, 0])
        else:
            self.rect = self.rect.move([-self.pas, 0])

    def right(self):
        if self.rect.right >= outils.SCREEN_WIDTH:
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
