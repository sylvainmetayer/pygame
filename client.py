#!/usr/bin/python2
# -*- coding: utf-8 -*-

import pygame
import sys
from pygame.locals import *

from PodSixNet.Connection import connection, ConnectionListener

import outils
from Balle import BallClient
from Bar import BarClient, BarsClient
from Brique import BriquesClient
from Tir import TirsClient


class Client(ConnectionListener):
    def __init__(self, host, port):
        self.Connect((host, port))
        self.game_client = True
        self.end = 3
        self.shotAllowed = True

    def Loop(self):
        connection.Pump()
        self.Pump()


    def Network(self, data):
        # ('message de type %s recu' % data['action'])
        pass

    def Network_isAllowedToShot(self, data):
        self.shotAllowed = data['value']
        print "MEGALOL" + str(self.shotAllowed)

    def Network_info(self, data):
        message = data["message"]
        if message == "perdu":
            self.end = 2
            self.game_client = False
        if message == "gagne":
            self.game_client = False
            self.end = 1

    def Network_sound(self, data):
        if outils.ALLOW_SOUND:
            pygame.mixer.Sound("son/"+data["message"]).play()

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

    if len(sys.argv) == 3:
        port = sys.argv[2]
        ip = sys.argv[1]
    else:
        port = outils.PORT
        ip = outils.IP


    # Initialisation Pygame
    pygame.init()
    clock = pygame.time.Clock()

    # Instanciation des composants du jeu.
    client = Client(ip, int(port))
    balle = BallClient()

    # Pour autoriser la répétition des touches pressées
    pygame.key.set_repeat(1, 2000)

    # Fond du jeu
    background_image, background_rect = outils.Fonction.load_png('images/background.jpg')
    background_load, background_load_rect = outils.Fonction.load_png("images/loading.jpg")
    background_win, background_win_rect = outils.Fonction.load_png("images/win.jpg")
    background_loose, background_loose_rect = outils.Fonction.load_png("images/loose.jpg")

    # Image de waiting shot
    background_shot, background_shot_rect = outils.Fonction.load_png("images/red_point.png")

    # Barre
    bar = BarClient()
    bars = BarsClient()
    bars.add(bar)
    briques = BriquesClient()

    #Depart de la musique
    pygame.mixer.music.load("son/music.mp3")
    pygame.mixer.music.set_volume(0.3)

    if outils.ALLOW_SOUND:
        pygame.mixer.music.play(-1)

    tir_sprites = TirsClient()

    # Boucle de jeu principale
    while client.game_client:
        clock.tick(60)

        # IMPORTANT : pump de la connexion
        client.Loop()
        bars.update()
        balle.update()
        briques.update()
        tir_sprites.update()

        # Pour quitter
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit(0)

        if len(bars) == 2:
            # Récupération des touches
            touches = pygame.key.get_pressed()

            if touches[K_m]:
                if outils.ALLOW_SOUND:
                    outils.ALLOW_SOUND = False
                    pygame.mixer.music.pause()
                else:
                    outils.ALLOW_SOUND = True
                    pygame.mixer.music.unpause()

            # Notification au serveur
            client.Send({"action": "keys", "keys": touches})
            # On dessine
            if client.end == 3:
                screen.blit(background_image, background_rect)

                if client.shotAllowed:
                    screen.blit(background_shot, (250,250))
                screen.blit(balle.image, balle.rect)

                bars.draw(screen)
                briques.draw(screen)
                tir_sprites.draw(screen)
        else:
            screen.blit(background_load, background_load_rect)

        # IMPORTANT
        pygame.display.flip()

    pygame.mixer.music.stop()
    if client.end == 2:
        if outils.ALLOW_SOUND:
            pygame.mixer.Sound("son/win.wav").play()
    if client.end == 1:
        if outils.ALLOW_SOUND:
            pygame.mixer.Sound("son/loose.wav").play()

    if client.end == 2:
        screen.blit(background_win, background_win_rect)
    if client.end == 1:
        screen.blit(background_loose, background_loose_rect)
    pygame.display.flip()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit(0)


if __name__ == '__main__':
    main()
    sys.exit(0)
