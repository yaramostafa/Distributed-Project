import random
from time import sleep
import pygame
import pickle
import socket


class Game:

    def __init__(self, number_of_players, name):
        self.number_of_players = number_of_players
        self.players = []
        # Create Player List of names in DB
        self.name = name
        self.status = 0
        # Range from 0 to 2


class Player:
    def __init__(self,Player_name,Player_num):

        self.filepath = '.\\img\\car'+str(Player_num)+'.png'
        self.car_x_coordinate = (1300 * (0.1+0.2*(Player_num-1)))
        self.car_y_coordinate = (600 * 0.8)
        self.car_width = 49
        self.Player_name = Player_name
        self.Player_num = Player_num
        self.disconnect = 0
        self.count = 0
        self.game = None

    def create_game(self,number_of_players,name):
        g = Game(number_of_players,name)
        g.players.append(self.name)
        #Create Game in DB
        self.game = g

    def get_game(self):
        return self.game





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
