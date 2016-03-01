#!/usr/bin/python2
# -*- coding: utf-8 -*-

import os
import pygame
import sys
import time
from pygame.locals import *
import outils

from PodSixNet.Channel import Channel
from PodSixNet.Server import Server



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
        self.rect.center  = position


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
        # print('message de type %s recu' % data['action'])
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


class MyServer(Server):
    channelClass = ClientChannel

    def __init__(self, *args, **kwargs):
        Server.__init__(self, *args, **kwargs)
        self.clients = Bars()
        # self.run = False
        pygame.init()
        print('Le serveur démarre.')

    def Connected(self, channel, addr):
        self.clients.add(channel)
        if len(self.clients) == 1:
            print 'Je set la pos du J1'
            clientTmp = self.clients.__getitem__(0)
            clientTmp.bar.set_position(outils.POS_J1)
        elif len(self.clients) == 2:
            print "Je set la pos du J2"
            clientTmp = self.clients.__getitem__(1)
            clientTmp.bar.set_position(outils.POS_J2)
        else: # Joueur 2
            print "La partie est pleine."
            channel.Send({"action":"error", "error":"La partie est pleine"})
        print 'Un client se connecte'
        # self.run = True

    def update_bar(self):
        for client in self.clients:
            client.update_bar()

    def get_positions_bars(self):
        """
        TODO fonction qui retourne la liste de toutes les positions des barres
        :return:
        """
        liste = []
        for client in self.clients:
            liste.append(client.bar.rect.center)
        return liste

    def send_bar(self):

        for client in self.clients:
            client.Send({"action": "bar", "liste": self.get_positions_bars()})

    def send_info(self, message):
        for client in self.clients:
            client.Send({"action":"info", "message":message})

    def launch_game(self):
        pygame.display.set_caption("Server")
        screen = pygame.display.set_mode((outils.SCREEN_WIDTH / 4, outils.SCREEN_HEIGHT / 4))
        background_image, background_rect = load_png('images/background.jpg')
        clock = pygame.time.Clock()

        while True:
            self.Pump()
            clock.tick(60)

            if len(self.clients) == 2:
                self.update_bar()
                self.send_bar()
            else:
                self.send_info("En atttente d'un autre joueur pour commencer la partie...")

            # On dessine
            screen.blit(background_image, background_rect)
            pygame.display.flip()

    def del_client(self, channel):
        print('client deconnecte')
        self.clients.remove(channel)


def main_prog():
    """
    Cette fonction crée le serveur et lance le jeu
    :return:
    """
    my_server = MyServer(localaddr=(sys.argv[1], int(sys.argv[2])))
    my_server.launch_game()


if len(sys.argv) != 3:
    print "Usage:", sys.argv[0], "host port"

if __name__ == '__main__':
    main_prog()
    sys.exit(0)
