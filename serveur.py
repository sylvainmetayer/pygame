#!/usr/bin/python2
# -*- coding: utf-8 -*-

import pygame
import sys
import time
from pygame.locals import *

from PodSixNet.Channel import Channel
from PodSixNet.Server import Server

import outils
from Balle import Ball
from Bar import Bar, Bars
from Brique import Briques, Brique
from Tir import Tirs, Tir


class ClientChannel(Channel, pygame.sprite.Sprite):
    """
    Cette classe gère un client, qui se connecte au serveur, et lui attribue un bar.
    """

    def __init__(self, *args, **kwargs):
        Channel.__init__(self, *args, **kwargs)
        pygame.sprite.Sprite.__init__(self)
        self.bar = Bar()
        self.tirCompteurTmp = outils.FREQUENCE_TIR
        self.shotAllowed = True
        self.tir_sprites = Tirs()
        self.joueur = outils.J1

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
        if touches[K_SPACE]:
            if self.shotAllowed:
                tir = Tir(self.bar)
                self.tir_sprites.add(tir)
                self.shotAllowed = False
                self.tirCompteurTmp = outils.FREQUENCE_TIR
                self.send_info("sound", "shot.wav")
            else:
                if self.tirCompteurTmp >= 0:
                    self.tirCompteurTmp -= 1
                else:
                    self.shotAllowed = True

    def update_bar(self):
        self.bar.update()
        self.tir_sprites.update(self.joueur)

    def send_info(self, action, message):
        print action + " - " + message
        self.Send({"action": action, "message": message})

    def get_bar(self):
        return self.bar


class MyServer(Server):
    channelClass = ClientChannel

    def __init__(self, *args, **kwargs):
        Server.__init__(self, *args, **kwargs)
        pygame.display.set_caption("Server")
        self.screen = pygame.display.set_mode(outils.SIZE_SERVEUR)

        self.briques = Briques()
        for i in range(10,outils.SCREEN_WIDTH,120):
            self.brique = Brique((i, outils.SCREEN_HEIGHT/2))
            self.briques.add(self.brique)
        self.clients = Bars()
        self.balle = Ball()
        self.endGame = 0
        self.spriteJ1 = pygame.sprite.RenderClear()
        self.spriteJ2 = pygame.sprite.RenderClear()
        # self.run = False
        pygame.init()

    def Connected(self, channel, addr):
        self.clients.add(channel)
        if len(self.clients) == 1:
            clientTmp = self.clients.__getitem__(outils.J1)
            clientTmp.bar.set_position(outils.POS_J1)
            clientTmp.joueur = outils.J1
            self.spriteJ1.add(clientTmp.bar)
        elif len(self.clients) == 2:  # Joueur 2
            clientTmp = self.clients.__getitem__(outils.J2)
            clientTmp.bar.set_position(outils.POS_J2)
            clientTmp.joueur = outils.J2
            self.spriteJ1.add(clientTmp.bar)
            self.send_info("info", "C'est parti !")
        else:  # Partie pleine
            channel.Send({"action": "error", "error": "La partie est pleine"})
            # self.run = True

    def get_shot(self):
        liste = []
        for client in self.clients:
            for tir in client.tir_sprites:
                liste.append(tir.rect.center)
        return liste

    def update_bar(self):
        for client in self.clients:
            client.update_bar()

    def send_shot(self):
        self.send_info("shot", self.clients.__getitem__(outils.J1).get_shot())
        self.send_info("shot", self.clients.__getitem__(outils.J2).get_shot())

    def remove_client(self, joueur):
        if joueur == outils.KILL_J1:
            self.clients.__getitem__(outils.J1).Send({"action":"info","message":"perdu"} )
            self.clients.__getitem__(outils.J2).Send({"action":"info","message":"gagne"} )
            self.clients.__getitem__(outils.J1).get_bar().kill()
            self.endGame = outils.J1

        if joueur == outils.KILL_J2:
            self.clients.__getitem__(outils.J1).Send({"action":"info","message":"gagne"} )
            self.clients.__getitem__(outils.J2).Send({"action":"info","message":"perdu"} )
            self.clients.__getitem__(outils.J2).get_bar().kill()
            self.endGame = outils.J2

    def update_balle(self):
        isBriqueHit = self.briques.gestion(self.balle)
        if isBriqueHit:
            self.send_info("sound", "break.wav")
        if self.brique.__sizeof__() == 0 :
            self.balle.speed += 1
        if not(isBriqueHit):
            isJoueurKill = self.balle.update(self.clients.__getitem__(outils.J1).get_bar(), self.clients.__getitem__(outils.J2).get_bar())
            if isJoueurKill == outils.KILL_J1:
                self.remove_client(outils.KILL_J1)

            elif isJoueurKill == outils.KILL_J2:
                self.remove_client(outils.KILL_J2)
            elif isJoueurKill == outils.PLAY_SOUND_VAR:
                self.send_info("sound", "bound.wav")

    def get_positions_bars(self):
        """
        Fonction qui retourne une liste de la position des joueurs.
        """
        liste = []
        for client in self.clients:
            liste.append(client.bar.rect.center)
        return liste

    def get_positions_briques(self):
        liste = []
        for brique in self.briques:
            liste.append(brique.rect.center)
        return liste

    def send_briques(self):
        for client in self.clients:
            print "Briques \n\t"
            print self.get_positions_briques()
            client.Send({"action" : "briques", "liste":self.get_positions_briques()})

    def send_bar(self):
        for client in self.clients:
            print "Bar \n\t"
            print self.get_positions_bars()
            client.Send({"action": "bar", "liste": self.get_positions_bars()})

    def send_balle(self):
        for client in self.clients:
            print "Balle : \n\t"
            print self.balle.rect.center
            client.Send({"action": "balle", "center": self.balle.rect.center})
            print "Liste Tirs : \n\t"
            print self.get_shot()
            client.Send({"action": "shot", "liste":self.get_shot()})

    def send_info(self, action, message):
        """
        Cette méthode permet d'envoyer un message à tous les
        joueurs, en précisant le type et le contenu du message
        :param action: Type du message
        :param message: Généralement une String, pour informer de qqch
        :return:
        """
        for client in self.clients:
            print action + " - " +message
            client.Send({"action": action, "message": message})

    def get_all_clients(self):
        liste = []
        for client in self.clients:
            liste.append(client.bar)
        return liste

    def collide_ball(self, balle, bar):
        if balle.rect.colliderect(bar.rect) or balle.rect.colliderect(bar.rect):
            self.send_info("sound", "bound.wav")
            balle.deplacement()

    def del_client(self, channel):
        self.clients.remove(channel)

    def check_collision_tir_player(self):
        for tir in self.clients.__getitem__(outils.J1).tir_sprites:
            if pygame.sprite.collide_rect(tir, self.clients.__getitem__(outils.J2).get_bar()):
                # Collision joueur - tir 1
                self.remove_client(outils.KILL_J1)
        for tir in self.clients.__getitem__(outils.J2).tir_sprites:
            if pygame.sprite.collide_rect(tir, self.clients.__getitem__(outils.J1).get_bar()):
                # Collision joueur - tir 1
                self.remove_client(outils.KILL_J2)

    def launch_game(self):
        screen = self.screen
        background_image, background_rect = outils.Fonction.load_png('images/background.jpg')
        background_load, background_load_rect = outils.Fonction.load_png("images/loading_mini.gif")
        clock = pygame.time.Clock()

        # Petit Timer pour eviter un début du jeu trop brutal
        gameStart = False

        while True:
            self.Pump()

            if self.endGame != 0:
                if self.endGame == outils.J1:
                    self.clients.remove(self.clients.__getitem__(outils.J1))
                if self.endGame == outils.J2:
                    self.clients.remove(self.clients.__getitem__(outils.J2))

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
                pygame.sprite.groupcollide(self.briques, self.clients.__getitem__(outils.J1).tir_sprites, False, True, pygame.sprite.collide_circle_ratio(0.7))
                pygame.sprite.groupcollide(self.briques, self.clients.__getitem__(outils.J2).tir_sprites, False, True, pygame.sprite.collide_circle_ratio(0.7))
                self.update_balle()
                self.check_collision_tir_player()
                self.send_bar()
                self.send_balle()
                self.send_briques()

                print "-----------------------------------------"

                screen.blit(background_image, background_rect)
            else:
                screen.blit(background_load, background_load_rect)

            # On dessine
            pygame.display.flip()


def main_prog():
    if len(sys.argv) == 3:
        port = sys.argv[2]
        ip = sys.argv[1]
    else:
        port = outils.PORT
        ip = outils.IP

    print "IP : " + ip + "\tPort : " + str(port)
    my_server = MyServer(localaddr=(ip, int(port)))
    my_server.launch_game()

if __name__ == '__main__':
    main_prog()
    sys.exit(0)
