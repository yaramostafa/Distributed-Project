import random
from time import sleep
import pygame
import pickle
import socket, threading
from cargame import *

class ClientSocket:
    def __init__(self):
        host = 'localhost'
        port = 10000
        self.size = 2048

        self.csocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.csocket.connect((host, port))
        self.player = pickle.loads(self.csocket.recv(self.size))

    def send(self, data):
        try:
            self.csocket.send(pickle.dumps(data))
            return pickle.loads(self.csocket.recv(self.size))
        except:
            pass

class CarRacing:

    def __init__(self):
        pygame.init()
        self.display_width = 1300
        self.display_height = 600
        self.black = (0, 0, 0)
        self.white = (255, 255, 255)
        self.clock = pygame.time.Clock()
        self.gameDisplay = None
        self.client = ClientSocket()
        self.player = self.client.player
        self.carImg = pygame.image.load(self.player.filepath)
        self.initialize()


    def initialize(self):

        self.crashed = False

        # car
        #self.player = Player(4)#(self.display_width,self.display_height)

        # enemy_car
        self.enemy_car = pygame.image.load('.\\img\\enemy_car_1.png')
        self.enemy_car_startx = random.randrange(50, 950)
        self.enemy_car_starty = -600
        self.enemy_car_speed = 5
        self.enemy_car_width = 49
        self.enemy_car_height = 100

        # enemy_car2
        self.enemy_car2 = pygame.image.load('.\\img\\enemy_car_2.png')
        self.enemy_car2_startx = random.randrange(50, 950)
        self.enemy_car2_starty = -600
        self.enemy_car2_speed = 8
        self.enemy_car2_width = 49
        self.enemy_car2_height = 100

        # Background
        self.bgImg = pygame.image.load(".\\img\\back_ground.jpg")
        self.bg_x1 = 0#(self.display_width / 2) - (1046 / 2)
        self.bg_x2 = 0 #(self.display_width / 2) - (1046 / 2)
        self.bg_y1 = 0
        self.bg_y2 = -600
        self.bg_speed = 3
        self.count = 0

    def car(self, car_x_coordinate, car_y_coordinate):
        self.gameDisplay.blit(self.carImg, (car_x_coordinate, car_y_coordinate))

    def drawOpp(self):
        for opponent in self.opponents:
            if isinstance(opponent,Player):
                op_carImg = pygame.image.load(opponent.filepath)
                self.gameDisplay.blit(op_carImg, (opponent.car_x_coordinate, opponent.car_y_coordinate))

    def racing_window(self):
        self.gameDisplay = pygame.display.set_mode((self.display_width, self.display_height))
        pygame.display.set_caption('Car Dodge')
        self.run_car()

    def run_car(self):
        while not self.crashed:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.crashed = True

                if (event.type == pygame.KEYDOWN):
                    if (event.key == pygame.K_UP):
                        self.player.car_y_coordinate -= 50
                        print("CAR Y COORDINATES: %s" % self.player.car_y_coordinate)
                    if (event.key == pygame.K_DOWN):
                        self.player.car_y_coordinate += 50
                        print("CAR Y COORDINATES: %s" % self.player.car_y_coordinate)
                    if (event.key == pygame.K_LEFT):
                        self.player.car_x_coordinate -= 50
                        print("CAR X COORDINATES: %s" % self.player.car_x_coordinate)
                    if (event.key == pygame.K_RIGHT):
                        self.player.car_x_coordinate += 50
                        print("CAR X COORDINATES: %s" % self.player.car_x_coordinate)
                    print("x: {x}, y: {y}".format(x=self.player.car_x_coordinate, y=self.player.car_y_coordinate))

            self.gameDisplay.fill(self.black)
            self.back_ground_road()

            self.run_enemy_car(self.enemy_car_startx, self.enemy_car_starty)
            self.run_enemy2_car(self.enemy_car2_startx, self.enemy_car2_starty)
            self.enemy_car_starty += self.enemy_car_speed
            self.enemy_car2_starty += self.enemy_car2_speed

            if self.enemy_car_starty > self.display_height:
                self.enemy_car_starty = 0 - self.enemy_car_height
                self.enemy_car_startx = random.randrange(50, 950)

            if self.enemy_car2_starty > self.display_height:
                self.enemy_car2_starty = 0 - self.enemy_car_height
                self.enemy_car2_startx = random.randrange(50, 950)

            self.opponents = self.client.send(self.player)
            self.drawOpp()
            self.car(self.player.car_x_coordinate, self.player.car_y_coordinate)

            self.highscore(self.count)
            self.count += 1
            if (self.count % 100 == 0):
                # self.enemy_car_speed += 1
                # self.bg_speed += 1
                print("Milestone Reached!")
            if self.player.car_y_coordinate < self.enemy_car_starty + self.enemy_car_height:
                if self.player.car_x_coordinate > self.enemy_car_startx and self.player.car_x_coordinate < self.enemy_car_startx + self.enemy_car_width or self.player.car_x_coordinate + self.player.car_width > self.enemy_car_startx and self.player.car_x_coordinate + self.player.car_width < self.enemy_car_startx + self.enemy_car_width:
                    self.crashed = True
                    self.display_message("Game Over !!!")

            if self.player.car_y_coordinate < self.enemy_car2_starty + self.enemy_car2_height:
                if self.player.car_x_coordinate > self.enemy_car2_startx and self.player.car_x_coordinate < self.enemy_car2_startx + self.enemy_car2_width or self.player.car_x_coordinate + self.player.car_width > self.enemy_car2_startx and self.player.car_x_coordinate + self.player.car_width < self.enemy_car2_startx + self.enemy_car2_width:
                    self.crashed = True
                    self.display_message("Game Over !!!")



            if self.player.car_x_coordinate < 50 or self.player.car_x_coordinate > 950:
                self.crashed = True
                self.display_message("Game Over !!!")

            pygame.display.update()
            self.clock.tick(60)

    def display_message(self, msg):
        font = pygame.font.SysFont("comicsansms", 72, True)
        text = font.render(msg, True, (255, 255, 255))
        self.gameDisplay.blit(text, (550 - text.get_width() // 2, 240 - text.get_height() // 2))
        self.display_credit()
        pygame.display.update()
        self.clock.tick(60)
        sleep(1)
        car_racing.initialize()
        car_racing.racing_window()

    def back_ground_road(self):
        self.gameDisplay.blit(self.bgImg, (self.bg_x1, self.bg_y1))
        self.gameDisplay.blit(self.bgImg, (self.bg_x2, self.bg_y2))

        self.bg_y1 += self.bg_speed
        self.bg_y2 += self.bg_speed

        if self.bg_y1 >= self.display_height:
            self.bg_y1 = -600

        if self.bg_y2 >= self.display_height:
            self.bg_y2 = -600

    def run_enemy_car(self, thingx, thingy):
        self.gameDisplay.blit(self.enemy_car, (thingx, thingy))

    def run_enemy2_car(self, thingx, thingy):
        self.gameDisplay.blit(self.enemy_car2, (thingx, thingy))

    def highscore(self, count):
        font = pygame.font.SysFont("arial", 20)
        text = font.render("Score : " + str(count), True, self.white)
        self.gameDisplay.blit(text, (0, 0))

    def display_credit(self):
        font = pygame.font.SysFont("lucidaconsole", 14)
        text = font.render("Thanks for playing!", True, self.white)
        self.gameDisplay.blit(text, (850, 560))


if __name__ == '__main__':

    car_racing = CarRacing()
    car_racing.racing_window()