import random
from time import sleep
import pygame
import pickle
import socket


class Game:
    game_counter = 0
    def __init__(self, number_of_players):
        self.number_of_players = number_of_players
        self.players = []
        self.player_counter = 0
        self.number = Game.game_counter
        Game.game_counter += 1
        self.start = 0
        self.end = 0

    def create_player(self):
        p = Player(self.player_counter+1)
        self.player_counter += 1
        self.players.append(p)
        return p


class Player:
    def __init__(self,Player_num):

        self.filepath = '.\\img\\car'+str(Player_num)+'.png'
        self.car_x_coordinate = (1300 * (0.1+0.2*(Player_num-1)))
        self.car_y_coordinate = (600 * 0.8)
        self.car_width = 49
        self.Player_num = Player_num
        self.disconnect = 0
        self.count = 0


class Enemy:
    def __init__(self):
        ranges = [(50, 130), (180, 390), (440, 650), (700, 910)]
        l1, l2 = ranges[random.randrange(0, len(ranges))]
        self.startx = random.randrange(l1, l2)
        self.starty = -600

    def getNewXY(self):
        ranges = [(50, 130), (180, 390), (440, 650), (700, 910)]
        l1, l2 = ranges[random.randrange(0, len(ranges))]
        self.startx = random.randrange(l1, l2)
        self.starty = 0 - self.enemy_car_height
