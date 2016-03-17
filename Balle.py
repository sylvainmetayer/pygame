#!/usr/bin/python2
# -*- coding: utf-8 -*-

import pygame.sprite

from PodSixNet.Connection import ConnectionListener

import outils

# PARTIE SERVEUR

class Ball(pygame.sprite.Sprite):
    """
    Classe représentant la bille du jeu côté serveur
    """

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image, self.rect = outils.Fonction.load_png('images/balle.png')
        self.rect.center = outils.POS_BALLE
        self.speed = [0, outils.BALL_SPEED]
        self.pas = 10
        self.direction = outils.BAS

    def Network_ball(self, data):
        self.rect.center = data['center']

    def isPointInsideRect(x, y, rect):
        if (x > rect.left) and (x < rect.right) and (y > rect.top) and (y < rect.bottom):
            return True
        else:
            return False

    def update(self, bar1, bar2):
        """
        Cette fonction permet de gérer le déplacement de la balle, et les collisions avec les deux bars
        :param bar1: Joueur 1
        :param bar2: Joueur 2
        :return:
        """

        collide_joueur1 = self.rect.move(self.speed).colliderect(bar1)
        collide_joueur2 = self.rect.move(self.speed).colliderect(bar2)

        if outils.COTE_GAUCHE >= self.rect.left:
            # Collision mur gauche
            if self.direction == outils.HAUT:
                self.rect.left = outils.COTE_GAUCHE + 1
                self.deplacement(outils.RIGHT_UP)
            else:
                self.rect.left = outils.COTE_GAUCHE + 1
                self.deplacement(outils.RIGHT_DOWN)
            return outils.PLAY_SOUND_VAR
        elif outils.COTE_DROIT <= self.rect.right:
            # Collision mur droit
            if self.direction == outils.HAUT:
                self.rect.right = outils.COTE_DROIT - 1
                self.deplacement(outils.LEFT_UP)
            else:
                self.rect.right = outils.COTE_DROIT - 1
                self.deplacement(outils.LEFT_DOWN)
            return outils.PLAY_SOUND_VAR
        elif outils.COTE_HAUT >= self.rect.top:
            return outils.KILL_J2;
        elif outils.COTE_BAS <= self.rect.bottom:
            return outils.KILL_J1;
        elif collide_joueur1 == 0 and collide_joueur2 == 0:
            # Pas de collision
            self.rect = self.rect.move(self.speed)
        else:
            # Collision avec une des deux bars
            if collide_joueur1 != 0:
                self.direction = outils.BAS
                # La balle a touché la barre du joueur 1
                centerJoueur = bar1.rect.center
                leftJoueur = bar1.rect.left
                rightJoueur = bar1.rect.right

            if collide_joueur2 != 0:
                self.direction = outils.HAUT
                # La balle a touché la barre du joueur 2
                centerJoueur = bar2.rect.center
                leftJoueur = bar2.rect.left
                rightJoueur = bar2.rect.right

            zoneRightMax = rightJoueur - outils.MARGE_ZONE
            zoneLeftMax = leftJoueur + outils.MARGE_ZONE

            if leftJoueur <= self.rect.center[0] <= zoneLeftMax:
                if collide_joueur1 != 0:
                    self.deplacement(outils.LEFT_DOWN)
                else:
                    self.deplacement(outils.LEFT_UP)

            elif rightJoueur >= self.rect.center[0] >= zoneRightMax:
                if collide_joueur1 != 0:
                    self.deplacement(outils.RIGHT_DOWN)
                else:
                    self.deplacement(outils.RIGHT_UP)

            elif collide_joueur1 != 0:
                self.deplacement(outils.DOWN)
            elif collide_joueur2 != 0:
                self.deplacement(outils.UP)
            return outils.PLAY_SOUND_VAR

    def deplacement(self, direction):
        self.speed = direction

    def reverse(self):
        if self.speed == outils.RIGHT_UP:
            self.deplacement(outils.RIGHT_DOWN)
        elif self.speed == outils.RIGHT_DOWN:
            self.deplacement(outils.RIGHT_UP)
        elif self.speed == outils.LEFT_UP:
            self.deplacement(outils.LEFT_DOWN)
        elif self.speed == outils.LEFT_DOWN:
            self.deplacement(outils.LEFT_UP)

    def reverseDirection(self):
        if self.direction == outils.HAUT:
            self.direction = outils.BAS
        else:
            self.direction = outils.HAUT

# PARTIE CLIENT

class BallClient(pygame.sprite.Sprite, ConnectionListener):
    '''
    Classe représentant la bille du jeu
    '''

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image, self.rect = outils.Fonction.load_png('images/balle.png')
        self.rect.center = outils.POS_BALLE
        # self.speed = [3, 3]
        # self.pas = 10

    def Network_balle(self, data):
        self.rect.center = data['center']

    def update(self):
        self.Pump()
