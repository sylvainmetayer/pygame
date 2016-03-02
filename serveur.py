#!/usr/bin/python2
# -*- coding: utf-8 -*-

import os
import pygame
import sys
import time
from pygame.locals import *

from PodSixNet.Channel import Channel
from PodSixNet.Server import Server

import outils

"""
TODO
- Chercher des images plus tard
- Faire bouger les vaisseaux en même temps
- Ajouter la balle et la gestion de mort en cas de sortie de l'écran.
- Ajouter les briques et la gestion de rebond.
- Ajouter la des monstres qui poppent via des briques speciales et de la mort de la barre adverse.
-
- ... ?
"""


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


class Bar(pygame.sprite.Sprite):
    """
    Classe représentant la barre d'un joueur, côté serveur.
    Attribut : une image, une position (le rect de l'image) et une vitesse.
    """

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image, self.rect = load_png('images/bar.png')

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


# TODO Le Sprite qui n'a rien a foutre la, mais qui fait fonctionner le jeu en multi :D
class ClientChannel(Channel, pygame.sprite.Sprite):
    """
    Cette classe gère un client, qui se connecte au serveur, et lui attribue un bar.
    """

    def __init__(self, *args, **kwargs):
        Channel.__init__(self, *args, **kwargs)
        pygame.sprite.Sprite.__init__(self)
        self.bar = Bar()

    def Close(self):
        self._server.del_client(self)

    def Network(self, data):
        pass

    def Network_keys(self, data):
        """
        Cette fonction permet de récupérer les mouvements du client, et de les traiter.
        :param data: Les données reçues du client.
        """
        touches = data['keys']
        if touches[K_RIGHT] or touches[K_d]:
            self.bar.right()
        if touches[K_LEFT] or touches[K_q]:
            self.bar.left()

            # def send_bar(self):
            # pass
            # Cela servira-t-il a qqch ?

    def update_bar(self):
        self.bar.update()

    def get_bar(self):
        return self.bar


class Ball(pygame.sprite.Sprite):
    """
    Classe représentant la bille du jeu côté serveur
    """

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image, self.rect = load_png('images/balle.png')
        self.rect.center = outils.POS_BALLE
        self.speed = [0, outils.BALL_SPEED]
        self.pas = 10

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

        print "Collide J1 : " + str(collide_joueur1)
        print "Collide J2 : " + str(collide_joueur2)

        if collide_joueur1 == 0 and collide_joueur2 == 0:
            self.rect = self.rect.move(self.speed)
            # Pas de collision
        else:
            if collide_joueur1 != 0:
                # La balle a touché la barre du joueur 1
                centerJoueur = bar1.rect.center
                print "DATA JOUEUR 1"
                leftJoueur = bar1.rect.left
                rightJoueur = bar1.rect.right

            if collide_joueur2 != 0:
                # La balle a touché la barre du joueur 2
                centerJoueur = bar2.rect.center
                print "DATA JOUEUR 2"
                leftJoueur = bar2.rect.left
                rightJoueur = bar2.rect.right

            print "Center : " + str(centerJoueur)
            print "Left : " + str(leftJoueur)
            print "Right : " + str(rightJoueur)

            print "DATA BALLE"
            print "Bottom : " + str(self.rect.bottom)
            print "Center : " + str(self.rect.center)
            print "Left : " + str(self.rect.left)
            print "Right : " + str(self.rect.right)

            zoneLeftMax = leftJoueur + 20
            if leftJoueur <= self.rect.bottom <= zoneLeftMax:
                print "ZONE gauche atteinte"
                if collide_joueur1 != 0:
                    self.reverse(outils.LEFT_UP)
                else:
                    self.reverse(outils.LEFT_DOWN)

            zoneRightMax = rightJoueur - 20
            if rightJoueur <= self.rect.bottom <= zoneRightMax:
                print "ZONE droite atteinte"
                if collide_joueur1 != 0:
                    self.reverse(outils.RIGHT_UP)
                else:
                    self.reverse(outils.RIGHT_DOWN)

            """
            TODO gestion plus fine, et modifier la fonction reverse de sorte à lui passer un argument
            genre 'left' 'right' 'topleft' ... et ainsi déplacer de plus de façon la balle
            """
            if collide_joueur1 != 0:
                self.reverse(outils.DOWN)
            elif collide_joueur2 != 0:
                self.reverse(outils.UP)

            # self.reverse()
            # Collision, on fait demi-tour !

            # GESTION DES BORDURES
            if self.rect.left <= 0:
                self.reverse(outils.RIGHT_UP)
            if self.rect.right >= outils.SCREEN_WIDTH:
                self.reverse(outils.LEFT_DOWN)

    def reverse(self, direction):
        print "SPEED " + str(self.speed)
        print "DIRECTION " + str(direction)
        self.speed = direction

        """
        if int(self.speed[0]) == 0 and int(self.speed[1]) == outils.BALL_SPEED:
            print "UP"
            self.speed = outils.GOTO_UP
        else:
            print "DOWN"
            self.speed = outils.GOTO_DOWN
        """


class MyServer(Server):
    channelClass = ClientChannel

    def __init__(self, *args, **kwargs):
        Server.__init__(self, *args, **kwargs)
        pygame.display.set_caption("Server")
        self.screen = pygame.display.set_mode(outils.SIZE_SERVEUR)
        self.clients = Bars()
        self.balle = Ball()
        # self.run = False
        pygame.init()
        print('Le serveur démarre.')

    def Connected(self, channel, addr):
        self.clients.add(channel)
        if len(self.clients) == 1:
            clientTmp = self.clients.__getitem__(outils.J1)
            clientTmp.bar.set_position(outils.POS_J1)
        elif len(self.clients) == 2:  # Joueur 2
            clientTmp = self.clients.__getitem__(outils.J2)
            clientTmp.bar.set_position(outils.POS_J2)
            self.send_info("gameStart", "C'est parti !")
        else:  # Partie pleine
            channel.Send({"action": "error", "error": "La partie est pleine"})
            # self.run = True

    def update_bar(self):
        for client in self.clients:
            client.update_bar()

    def update_balle(self):
        self.balle.update(self.clients.__getitem__(outils.J1).get_bar(), self.clients.__getitem__(outils.J2).get_bar())

    def get_positions_bars(self):
        """
        Fonction qui retourne une liste de la position des joueurs.
        """
        liste = []
        for client in self.clients:
            liste.append(client.bar.rect.center)
        return liste

    def send_bar(self):
        for client in self.clients:
            client.Send({"action": "bar", "liste": self.get_positions_bars()})

    def send_balle(self):
        for client in self.clients:
            client.Send({"action": "balle", "center": self.balle.rect.center})

    def send_info(self, action, message):
        """
        Cette méthode permet d'envoyer un message à tous les
        joueurs, en précisant le type et le contenu du message
        :param action: Type du message
        :param message: Généralement une String, pour informer de qqch
        :return:
        """
        for client in self.clients:
            client.Send({"action": action, "message": message})

    def get_all_clients(self):
        liste = []
        for client in self.clients:
            liste.append(client.bar)
        return liste

    def collide_ball(self, balle, bar):
        if balle.rect.colliderect(bar.rect) or balle.rect.colliderect(bar.rect):
            print "Collision "
            balle.reverse()
            """if dx > 0: # Moving right; Hit the left side of the wall
                self.rect.right = wall.rect.left
            if dx < 0: # Moving left; Hit the right side of the wall
                self.rect.left = wall.rect.right
            if dy > 0: # Moving down; Hit the top side of the wall
                self.rect.bottom = wall.rect.top
            if dy < 0: # Moving up; Hit the bottom side of the wall
                self.rect.top = wall.rect.bottom"""

    def launch_game(self):
        screen = self.screen
        background_image, background_rect = load_png('images/background.jpg')
        background_load, background_load_rect = load_png("images/loading_mini.gif")
        clock = pygame.time.Clock()

        # Petit Timer pour eviter un début du jeu trop brutal
        gameStart = False

        while True:
            self.Pump()
            clock.tick(60)

            # Pour permettre de quitter le serveur
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit(0)

            if len(self.clients) == 2:
                if not gameStart:
                    gameStart = True
                    self.send_info("info", "debut du jeu dans 3 secondes !")
                    time.sleep(3)

                self.update_bar()
                self.update_balle()
                self.send_bar()
                self.send_balle()

                # collisions joueur 1 avec la balle
                # self.collide_ball(self.balle, self.clients.__getitem__(outils.J1).get_bar())
                # self.collide_ball(self.balle, self.clients.__getitem__(outils.J2).get_bar())

                screen.blit(background_image, background_rect)
            else:
                screen.blit(background_load, background_load_rect)

            # On dessine
            pygame.display.flip()

    def del_client(self, channel):
        print('DISCONNECTED client')
        self.clients.remove(channel)


def main_prog():
    """
    Cette fonction crée le serveur et lance le jeu
    :return:
    """

    if len(sys.argv) == 2:
        port = sys.argv[2]
        ip = sys.argv[1]
    else:
        port = outils.PORT
        ip = outils.IP

    my_server = MyServer(localaddr=(ip, int(port)))
    my_server.launch_game()


if len(sys.argv) != 3:
    print "Usage:", sys.argv[0], "[host] [port]"

if __name__ == '__main__':
    main_prog()
    sys.exit(0)
