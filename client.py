#!/usr/bin/python2
# -*- coding: utf-8 -*-

import os
import pygame
import sys
from pygame.locals import *

from PodSixNet.Connection import connection, ConnectionListener

SCREEN_WIDTH = 1024
SCREEN_HEIGHT = 768


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



class Ship(pygame.sprite.Sprite, ConnectionListener):
    """
    Classe représentant le vaisseau côté client.
    """

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image, self.rect = load_png('Pics/ship.png')
        self.rect.center = [SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2]
        self.speed = [3, 3]
        self.pas = 10

    def Network_ship(self, data):
        self.rect.center = data['center']

    def update(self):
        self.Pump()


class Tir(pygame.sprite.Sprite):
    """
    Classe de tir
    """

    def __init__(self, coordonnees):
        pygame.sprite.Sprite.__init__(self)
        self.image, self.rect = load_png("Pics/shot.png");
        self.speed = [0, -1]
        self.rect.center = coordonnees

    def update(self):
        pass


class Tirs(pygame.sprite.Group, ConnectionListener):
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
        # print listeTir
        for xy in listeTir:
            tir = Tir(xy)
            self.add(tir)


class Client(ConnectionListener):
    def __init__(self, host, port):
        self.Connect((host, port))
        self.game_client = True

    def Loop(self):
        connection.Pump()
        self.Pump()

    def Network(self, data):
        # ('message de type %s recu' % data['action'])
        # print data
        pass

    ### Network event/message callbacks ###
    def Network_connected(self, data):
        print('connecte au serveur !')
        self.game_client = True;

    def Network_error(self, data):
        print 'error:', data['error'][1]
        connection.Close()
        self.game_client = False;

    def Network_disconnected(self, data):
        print 'Server disconnected'
        sys.exit()

def main():
    # Initialisation pygame
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    client = Client(sys.argv[1], int(sys.argv[2]))

    pygame.init()
    clock = pygame.time.Clock()
    pygame.key.set_repeat(1, 1)

    # On crée les objets
    background_image, background_rect = load_png('Pics/background.jpg')
    ship = Ship()  # creation d'une instance de Ship
    ship_sprites = pygame.sprite.RenderClear()  # creation d'un groupe de sprite
    ship_sprites.add(ship)
    tir_sprites = Tirs()

    while True:
        clock.tick(60)  # max speed is 60 frames per second
        client.Loop()

        # Si le client lance le jeu
        if client.game_client is True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit(0)

            # Récupération des touches
            touches = pygame.key.get_pressed()
            client.Send({"action": "keys", "keys": touches})

            # Refresh connexion + update
            ship_sprites.update()
            tir_sprites.update()

            # On dessine
            screen.blit(background_image, background_rect)
            ship_sprites.draw(screen)
            tir_sprites.draw(screen)
            pygame.display.flip()


if __name__ == '__main__':
    print "Je passe dans le main"
    main()
    sys.exit(0)
