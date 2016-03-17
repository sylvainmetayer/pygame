#!/usr/bin/python2
# -*- coding: utf-8 -*-

import pygame
import sys

from PodSixNet.Connection import connection, ConnectionListener

import outils
from Balle import BallClient
from Bar import BarClient, BarsClient
from Brique import BriquesClient


class Client(ConnectionListener):
    def __init__(self, host, port):
        self.Connect((host, port))
        self.game_client = True
        self.end = 0

    def Loop(self):
        connection.Pump()
        self.Pump()

    def Network(self, data):
        # ('message de type %s recu' % data['action'])
        # print data
        pass

    def Network_info(self, data):
        message = data["message"];
        tab = message.split(" ")
        if tab[0] == "perdu":
            self.end = 2
        if tab[0] == "gagne":
            self.end = 1

    def Network_connected(self, data):
        print('connecte au serveur !')
        self.game_client = True

    def Network_error(self, data):
        print 'error:', data['error'][1]
        connection.Close()
        self.game_client = False

    def Network_disconnected(self, data):
        print 'Server disconnected'
        sys.exit()


def main():
    # Initialisation de l'écran
    screen = pygame.display.set_mode((outils.SCREEN_WIDTH, outils.SCREEN_HEIGHT))

    if len(sys.argv) == 2:
        port = sys.argv[2]
        ip = sys.argv[1]
    else:
        port = outils.PORT
        ip = outils.IP

    # Instanciation des composants du jeu.
    client = Client(ip, int(port))
    balle = BallClient()

    # Initialisation Pygame
    pygame.init()
    clock = pygame.time.Clock()

    # Pour autoriser la répétition des touches pressées
    pygame.key.set_repeat(1, 1)

    # Fond du jeu
    background_image, background_rect = outils.Fonction.load_png('images/background.jpg')
    background_load, background_load_rect = outils.Fonction.load_png("images/loading.jpg")
    background_win, background_win_rect = outils.Fonction.load_png("images/win.jpg")
    background_loose, background_loose_rect = outils.Fonction.load_png("images/loose.jpg")

    # Barre
    bar = BarClient()
    bars = BarsClient()
    bars.add(bar)
    briques = BriquesClient()


    # Boucle de jeu principale
    while True:
        clock.tick(60)

        # IMPORTANT : pump de la connexion
        client.Loop()
        bars.update()
        balle.update()
        briques.update()

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
            if client.end == 0:
                screen.blit(background_image, background_rect)
                screen.blit(balle.image, balle.rect)
                bars.draw(screen)
                briques.draw(screen)
        else:
            print str(client.end)
            if client.end == 1:
                screen.blit(background_win, background_win_rect)
            elif client.end == 2:
                screen.blit(background_loose, background_loose_rect)
            else:
                screen.blit(background_load, background_load_rect)

        # IMPORTANT
        pygame.display.flip()


if __name__ == '__main__':
    main()
    sys.exit(0)
