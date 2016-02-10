#!/usr/bin/python2
# -*- coding: utf-8 -*-

import os
import pygame
import sys
import time
from pygame.locals import *

from PodSixNet.Channel import Channel
from PodSixNet.Server import Server

SCREEN_WIDTH = 1024
SCREEN_HEIGHT = 768

#Gestion Tirs
tirCompteurTmp = 30
shotAllowed = True


def load_png(name):
    """Load image and return image object"""
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


class Tir(pygame.sprite.Sprite):
    """
    Classe de tir du vaisseau
    """

    def __init__(self, ship):
        pygame.sprite.Sprite.__init__(self)
        self.image, self.rect = load_png('Pics/shot.png')
        self.speed = [0, -1]
        self.rect.center = ship.rect.center

    def update(self):
        """

        :return: True si le tir est mort, False sinon
        """
        self.rect = self.rect.move([0, -10])
        if self.rect.top <= -20:
            self.kill()
            return True;
        return False;


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


class Ship(pygame.sprite.Sprite):
    """
    Classe représentant le vaisseau côté serveur.
    """

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image, self.rect = load_png('Pics/ship.png')
        self.rect.center = [SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2]
        self.speed = [3, 3]
        self.pas = 10

    def up(self):
        if self.rect.top <= 0:
            self.rect = self.rect.move([0, 0])
        else:
            self.rect = self.rect.move([0, -self.pas])

    def down(self):
        if self.rect.bottom >= SCREEN_HEIGHT:
            self.rect = self.rect.move([0, 0])
        else:
            self.rect = self.rect.move([0, self.pas])
            # self.speed[1] += 1

    def left(self):
        if self.rect.left <= 0:
            self.rect = self.rect.move([0, 0])
        else:
            self.rect = self.rect.move([-self.pas, 0])
            # self.speed[0] -= 1

    def right(self):
        if self.rect.right >= SCREEN_WIDTH:
            self.rect = self.rect.move([0, 0])
        else:
            self.rect = self.rect.move([self.pas, 0])
            # self.speed[0] += 1

    def update(self):
        if self.speed[0] >= 5 or self.speed[0] >= -5:
            self.speed[0] = 0
        if self.speed[1] >= 5 or self.speed[1] >= -5:
            self.speed[1] = 0
        self.rect = self.rect.move(self.speed)


class ClientChannel(Channel):
    """
    Cette classe gère un client, qui se connecte au serveur, et lui attribue un vaisseau.
    """

    def __init__(self, *args, **kwargs):
        Channel.__init__(self, *args, **kwargs)

        # Gestion vaisseau
        self.ship = Ship()
        self.ship_sprite = pygame.sprite.RenderClear()
        self.ship_sprite.add(self.ship)

        # Gestion tirs
        self.tir_sprites = Tirs()

    def Close(self):
        self._server.del_client(self)

    def Network(self, data):
        # print('message de type %s recu' % data['action'])
        pass

    def Network_keys(self, data):
        """
        Cette fonction permet de récupérer les mouvements du client, et de les traiter.
        :param data:
        :return:
        """
        touches = data['keys']
        if touches[K_UP]:
            self.ship.up()
        if touches[K_q]:
            print "Le client s'est deconnecté du jeu"
            sys.exit(1)
        if touches[K_DOWN]:
            self.ship.down()
        if touches[K_RIGHT]:
            self.ship.right()
        if touches[K_LEFT]:
            self.ship.left()
        if touches[K_SPACE]:
            #if shotAllowed:
            shotAllowed = False
            tmp = tirCompteurTmp
            tir = Tir(self.ship)
            self.tir_sprites.add(tir)


    def send_shot(self):
        liste = []
        for tir in self.tir_sprites:
            liste.append(tir.rect.center)
        self.Send({"action": "shot", "liste": liste})

    def send_ship(self):
        self.Send({"action": "ship", "center": self.ship.rect.center})

    def update_ship(self):
        self.ship_sprite.update()
        self.tir_sprites.update()


class MyServer(Server):
    channelClass = ClientChannel

    def __init__(self, *args, **kwargs):
        Server.__init__(self, *args, **kwargs)
        self.clients = []
        self.run = False
        pygame.init()
        print('Server launched')

    def Connected(self, channel, addr):
        print('New connection')
        self.clients.append(channel)
        self.run = True

    def update_ship(self):
        for client in self.clients:
            client.update_ship()

    def send_ship(self):
        for client in self.clients:
            client.send_ship()

    def send_shot(self):
        for client in self.clients:
            client.send_shot();

    def launch_game(self):
        pygame.display.set_caption("Server")
        screen = pygame.display.set_mode((SCREEN_WIDTH / 4, SCREEN_HEIGHT / 4))
        background_image, background_rect = load_png('Pics/background.jpg')
        clock = pygame.time.Clock()


        #Gestion Tirs:


        while True:
            clock.tick(60)
            time.sleep(0.01)
            self.Pump()

            if self.run:
                self.update_ship()
                self.send_ship()
                self.send_shot()

            # Gestion Tirs
            tirCompteurTmp = tirCompteurTmp - 1
            if tirCompteurTmp <= 0:
                shotAllowed = True

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
