#!/usr/bin/python2
# -*- coding: utf-8 -*-

import os
import pygame
import sys

from PodSixNet.Connection import connection, ConnectionListener

import outils


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
    '''
    Classe représentant la bar sur laquelle la balle rebondit
    '''

    def __init__(self, center=(outils.SCREEN_WIDTH/2, outils.SCREEN_HEIGHT/2)):
        pygame.sprite.Sprite.__init__(self)
        self.image, self.rect = load_png('images/bar.png')
        self.rect.center = center
        self.speed = [3, 3]
        self.pas = 10

    def update(self):
        pass


class Bars(pygame.sprite.Group, ConnectionListener):
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
        print data
        for xy in donnees:
            bar = Bar(xy)
            self.add(bar)

class Ball(pygame.sprite.Sprite, ConnectionListener):
    '''
    Classe représentant la bille du jeu
    '''
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image, self.rect = load_png('images/balle.png')
        self.rect.center = outils.POS_BALLE
        #self.speed = [3, 3]
        #self.pas = 10

    def Network_balle(self, data):
        self.rect.center = data['center']

    def update(self):
        self.Pump()

#class Brick(pygame.sprite.Sprite, ConnectionListener):
    '''
    Classe représentant une brique à casser
    '''

class Client(ConnectionListener):
    def __init__(self, host, port):
        self.Connect((host, port))
        self.game_client = True

    def Loop(self):
        connection.Pump()
        self.Pump()

    def Network(self, data):
        #('message de type %s recu' % data['action'])
        print data
        pass

    def Network_info(self,data):
        print data['message']

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
    # Initialisation de l'écran
    screen = pygame.display.set_mode((outils.SCREEN_WIDTH, outils.SCREEN_HEIGHT))

    """
    Récupération IP / PORT :
        - de la ligne de commande
        OU
        - du fichier de configuration
    """
    if len(sys.argv) == 2:
        port = sys.argv[2]
        ip = sys.argv[1]
    else:
        port = outils.PORT
        ip = outils.IP

    # Instanciation des composants du jeu.
    client = Client(ip, int(port))
    balle = Ball()

    # Initialisation Pygame
    pygame.init()
    clock = pygame.time.Clock()

    # Pour autoriser la répétition des touches pressées
    pygame.key.set_repeat(1, 1)

    # Fond du jeu
    background_image, background_rect = load_png('images/background.jpg')
    background_load, background_load_rect = load_png("images/loading.jpg")

    # Barre
    bar = Bar()  # creation d'une instance de Bar
    bars = Bars()
    bars.add(bar)

    # Boucle de jeu principale
    while True:
        clock.tick(60)  # max speed is 60 frames per second

        # IMPORTANT : pump de la connexion
        client.Loop()
        bars.update()
        balle.update()

        # Pour quitter
        for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit(0)

        if len(bars) == 2:
        # 2 joueurs, la partie peut commencer

            # Récupération des touches
            touches = pygame.key.get_pressed()

            # Notification au serveur
            client.Send({"action": "keys", "keys": touches})

            # On dessine
            screen.blit(background_image, background_rect)
            bars.draw(screen)
            screen.blit(balle.image, balle.rect)
        else:
            # On affiche un loader
            screen.blit(background_load, background_load_rect)

        # IMPORTANT : C'est ça qui affiche à l'écran.
        pygame.display.flip()

if __name__ == '__main__':
    main()
    sys.exit(0)
