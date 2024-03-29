import random, pygame, socket, threading, ChatClient as CC, ClientFunctions as CF
import SocketUtils as SU
from time import sleep

HOST = 'localhost'
PORT = 10000
MSGSIZE = 2048
import atexit

def exitClient(csocket):
    csocket.closeconn()
    print("exiting now, goodbye")

class ClientSocket:
    def __init__(self):
        self.csocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.csocket.connect((HOST, PORT))
        #login/signup
        
        chooseLogin = int(input('Choose 1 to signup or 2 to login:'))
        while True:
            if not (chooseLogin == 1 or chooseLogin ==2):
                chooseLogin = int(input('Please enter a correct choice: '))
            else: break
        print(chooseLogin)
        SU.send(self.csocket, chooseLogin)
        cName = ""
        if chooseLogin==2:
            cName = CF.cLogin(self.csocket)
        elif chooseLogin==1:
            cName = CF.cSignup(self.csocket)+ "'s Chat"
        # t1 = threading.Thread(target=CC.initChat, args=(cName, ))
        # t1.start()
        
        self.player = SU.receiveArr(self.csocket)
        self.player[0] = int(self.player[0])
        self.player[2] = int(self.player[2])
        self.player[3] = int(self.player[3])
        self.player[4] = int(self.player[4])
        self.player[5] = int(self.player[5])
        self.player[6] = int(self.player[6])
        self.player[7] = int(self.player[7])
        SU.send(self.csocket, 0)
        atexit.register(exitClient, self.csocket)
        

    def send(self, data):
        try:
            SU.sendArr(self.csocket, data)
            size = SU.receiveInt(self.csocket)
            buf = []
            for _ in range(size):
                SU.send(self.csocket, 0)
                rec = SU.receiveArr(self.csocket)
                rec[0] = int(rec[0])
                rec[2] = int(rec[2])
                rec[3] = int(rec[3])
                rec[4] = int(rec[4])
                rec[5] = int(rec[5])
                rec[6] = int(rec[6])
                rec[7] = int(rec[7])
                buf += [rec]
            return buf
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
        print(self.player)
        self.carImg = pygame.image.load(self.player[-1])
        self.initialize()

    def initialize(self):

        self.crashed = False

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

        # Blurred Background
        self.bgImgB = pygame.image.load(".\\img\\blurred.jpg")
        self.bg_x1b = 0  # (self.display_width / 2) - (1046 / 2)
        self.bg_x2b = 0  # (self.display_width / 2) - (1046 / 2)
        self.bg_y1b = 0
        self.bg_y2b = -600

    def car(self, car_x_coordinate, car_y_coordinate):
        self.gameDisplay.blit(self.carImg, (car_x_coordinate, car_y_coordinate))

    def drawOpp(self):
        for opponent in self.opponents:
            if opponent[-2] == 0:
                op_carImg = pygame.image.load(opponent[-1])
                self.gameDisplay.blit(op_carImg, (opponent[4], opponent[5]))

    def racing_window(self):
        self.gameDisplay = pygame.display.set_mode((self.display_width, self.display_height))
        pygame.display.set_caption('Waiting Screen')
        self.waitingForPlayers()
        pygame.display.set_caption('Car Dodge')
        self.run_car()
        

    def run_car(self):
        win = -1
        while not self.crashed:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.crashed = True
                    SU.send(self.client.csocket, 0)
                    pygame.quit()
                    
                
                if (event.type == pygame.KEYDOWN):
                    if (event.key == pygame.K_LEFT):
                        self.player[4] -= 50
                    if (event.key == pygame.K_RIGHT):
                        self.player[4] += 50

            self.gameDisplay.fill(self.black)
            self.back_ground_road()

            self.run_enemy_car(self.enemy_car_startx, self.enemy_car_starty)
            self.run_enemy2_car(self.enemy_car2_startx, self.enemy_car2_starty)
            self.enemy_car_starty += self.enemy_car_speed
            self.enemy_car2_starty += self.enemy_car2_speed

            if self.enemy_car_starty > self.display_height:
                self.enemy_car_starty = 0 - self.enemy_car_height
                self.enemy_car_sttx = random.randrange(50, 950)

            if self.enemy_car2_starty > self.display_height:
                self.enemy_car2_starty = 0 - self.enemy_car_height
                self.enemy_car2_startx = random.randrange(50, 950)



            self.opponents = self.client.send(self.player)
            self.drawOpp()
            self.car(self.player[4], self.player[5])

            self.highscore(self.player[6])
            win = self.leaderboard()
            if win != -1:
                self.display_winner(self.player[1])
                break
            self.player[6] += 1
            if (self.player[6] % 100 == 0):
                self.enemy_car_speed += 1
                self.bg_speed += 1
                print("Milestone Reached!")
            if self.player[5] < self.enemy_car_starty + self.enemy_car_height:
                if self.player[5] > self.enemy_car_startx and self.player[4] < self.enemy_car_startx + self.enemy_car_width or self.player[4] + 49 > self.enemy_car_startx and self.player[4] + 49 < self.enemy_car_startx + self.enemy_car_width:
                    self.crashed = True
                    #self.display_message("Game Over !!!")
                    self.player[6]-= 100
                    self.display_message("Crashed -100")

            if self.player[5] < self.enemy_car2_starty + self.enemy_car2_height:
                if self.player[4] > self.enemy_car2_startx and self.player[4] < self.enemy_car2_startx + self.enemy_car2_width or self.player[4] + 49 > self.enemy_car2_startx and self.player[4] + 49 < self.enemy_car2_startx + self.enemy_car2_width:
                    self.crashed = True
                    #self.display_message("Game Over !!!")
                    self.player[6] -= 100
                    self.display_message("Crashed -100")

            if self.player[4] < 50 or self.player[4] > 950:
                self.crashed = True
                self.player[6] -= 1000
                self.display_message("Out Of Bound -1000")

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
        car_racing.run_car()

    def display_winner(self, winner):
        font = pygame.font.SysFont("comicsansms", 72, True)
        winning_msg = winner+" has won the race!!!"
        text = font.render(winning_msg, True, (255, 255, 255))
        self.gameDisplay.blit(text, (550 - text.get_width() // 2, 240 - text.get_height() // 2))
        self.display_credit()
        pygame.display.update()
        self.clock.tick(60)
        car_racing.initialize()
        SU.send(self.client.csocket, 0)

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

    def highscore(self, score):
        font = pygame.font.SysFont("arial", 20)
        text = font.render("Score : " + str(score), True, self.white)
        self.gameDisplay.blit(text, (0, 0))

    def leaderboard(self):
        all_scores = []
        dis = 100
        disconnected = []
        for opponent in self.opponents:
            print("OPPONENT: ",opponent[-2])
            if opponent[-2] == 1:
                font = pygame.font.SysFont("arial", 20)
                disconnectMsg = "Player"+str(opponent[3])+" Disconnected"
                text = font.render(disconnectMsg, True, self.white)
                self.gameDisplay.blit(text, (1055, dis))
                disconnected.append(opponent[3]-1)
                dis -= 20
            else:
                all_scores.append(opponent[6])

        all_scores.insert(self.player[3]-1, self.player[6])
        all_scores_sorted = all_scores.copy()

        all_scores_sorted.sort(reverse=True)
        
        font = pygame.font.SysFont("arial", 20)
        text = font.render("LEADERBOARD", True, self.white)
        self.gameDisplay.blit(text, (1055, 0))
        
        i = 20
        for d in disconnected:
            all_scores.insert(d,"d")
        print(all_scores)
        players = []
        for score in all_scores_sorted:
            player = all_scores.index(score)+1
            players.append(player)
            rank = all_scores_sorted.index(score) + 1
            all_scores[player-1] = -1
            font = pygame.font.SysFont("arial", 20)
            msg = str(rank)+".Player"+str(player)+": "+str(score)
            #print(msg)
            text = font.render(msg, True, self.white)
            self.gameDisplay.blit(text, (1055, i))
            i+=20
        if all_scores_sorted[0] >= 20000:
            return str(all_scores_sorted[0])
        else:
            return -1

    def display_credit(self):
        font = pygame.font.SysFont("lucidaconsole", 14)
        text = font.render("Thanks for playing!", True, self.white)
        self.gameDisplay.blit(text, (850, 560))

    def waitingForPlayers(self):

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
        self.gameDisplay.fill(self.black)
        recieved = SU.receiveString(self.client.csocket)
        font = pygame.font.SysFont("lucidaconsole", 40)
        text = font.render("Waiting for players... ^.^", True, self.white)
        self.gameDisplay.blit(text, (550 - text.get_width() // 2, 240 - text.get_height() // 2))
        pygame.display.update()
        self.clock.tick(60)

        while recieved != "start":
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()

            self.gameDisplay.fill(self.black)
            recieved = SU.receiveString(self.client.csocket)
            font = pygame.font.SysFont("lucidaconsole", 40)
            text = font.render("Waiting for players... ^.^", True, self.white)
            self.gameDisplay.blit(text, (550 - text.get_width() // 2, 240 - text.get_height() // 2))
            pygame.display.update()
            self.clock.tick(60)




if __name__ == '__main__':

    car_racing = CarRacing()
    car_racing.racing_window()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
