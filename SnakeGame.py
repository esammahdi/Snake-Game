import sys
import time
import json
import random
import pygame
from pygame.locals import *

# Global Fields
SCREEN = (800, 600)
FPS = 60
SPEED = 0.36
SCORE = 0
SIZE = 10
YemekSize = SIZE + 4
SEPERATION = 4
scores = {}

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

# pygame
pygame.init()
pygame.display.set_caption("Yilan Oyunu")
surface = pygame.display.set_mode(SCREEN)
clock  = pygame.time.Clock()

# Big thanks to @youtube 'Techie Coder' for his snake game tutorial. His code was really helpful in understanding and making this project

# Snake Class

class Yilan() :
    def __init__(self):
        self.body = [[SCREEN[0] // 2,SCREEN[1] // 2,'UP']]

    def move(self):
        for i in range(len(self.body) - 1,0,-1):

            self.body[i][2] = self.body[i - 1][2]
            self.body[i][1] = self.body[i - 1][1]
            self.body[i][0] = self.body[i - 1][0]

        last_segment = self.body.pop(0)

        if last_segment[2] == 'UP':
            last_segment[1] -= SIZE * SPEED
        elif last_segment[2] == 'DOWN':
            last_segment[1] += SIZE * SPEED
        elif last_segment[2] == 'RIGHT':
            last_segment[0] += SIZE * SPEED
        else:
            last_segment[0] -= SIZE * SPEED

        self.body.insert(0, last_segment)

    def grow(self):
        last = self.body[len(self.body) - 1]

        if(last[2] == 'UP'):
            self.body.append([last[0] , last[1] - SIZE - SEPERATION, last[2]])
        elif (last[2] == 'DOWN'):
            self.body.append([last[0] , last[1] + SIZE + SEPERATION, last[2]])
        elif (last[2] == 'RIGHT'):
            self.body.append([last[0] + SIZE + SEPERATION, last[1], last[2]])
        else:
            self.body.append([last[0] - SIZE - SEPERATION, last[1], last[2]])

        pygame.mixer.Sound('res/eat.wav').play()

    def checkCollision(self):
        rect = pygame.Rect(self.body[0][0],self.body[0][1],SIZE,SIZE)

        for i in range (5,len(self.body)):
            collision = rect.colliderect(pygame.Rect(self.body[i][0],self.body[i][1],SIZE,SIZE))
            if(collision) :
                return True
        return False

    def checkScreenSides(self):
        if self.body[0][0] > SCREEN[0]:
            self.body[0][0] = SIZE
        if self.body[0][0] < 0:
            self.body[0][0] = SCREEN[0] - SIZE
        if self.body[0][1] > SCREEN[1]:
            self.body[0][1] = SIZE
        if self.body[0][1] < 0:
            self.body[0][1] = SCREEN[1] - SIZE

    def setDirection(self,direction):
        if (self.body[0][2] == "RIGHT" and direction == "LEFT" or self.body[0][2] == "LEFT" and
                direction == "RIGHT"):
            pass
        elif (self.body[0][2] == "UP" and direction == "DOWN" or self.body[0][2] == "DOWN" and
              direction == "UP"):
            pass
        else:
            self.body[0][2] = direction

    def draw(self):

        pygame.draw.rect(surface, GREEN, (self.body[0][0], self.body[0][1],
                                          SIZE, SIZE),0)

        counter = 1
        while counter < len(self.body):
            pygame.draw.rect(surface, BLUE, (self.body[counter][0], self.body[counter][1],
                                             SIZE, SIZE),0)
            counter += 1

# Food Class
class Yemek() :
    def __init__(self):
        self.random()

    def random(self):
        self.x = random.randint(50,SCREEN[0] - 50)
        self.y = random.randint(50, SCREEN[1] - 50)

    def draw(self):
        pygame.draw.rect(surface,RED,(self.x,self.y,YemekSize,YemekSize))

# Big thanks to @youtube 'Clean Code' for providing the Button class which was used in creating the menus
class Button:
	def __init__(self,text,width,height,pos,elevation):
		#Core attributes
		self.pressed = False
		self.elevation = elevation
		self.dynamic_elecation = elevation
		self.original_y_pos = pos[1]
        # self.screen = screen

		# top rectangle
		self.top_rect = pygame.Rect(pos,(width,height))
		self.top_color = '#475F77'

		# bottom rectangle
		self.bottom_rect = pygame.Rect(pos,(width,height))
		self.bottom_color = '#354B5E'
		#text
		self.text_surf = pygame.font.Font(None,30).render(text,True,'#FFFFFF')
		self.text_rect = self.text_surf.get_rect(center = self.top_rect.center)

	def draw(self):
		# elevation logic
		self.top_rect.y = self.original_y_pos - self.dynamic_elecation
		self.text_rect.center = self.top_rect.center

		self.bottom_rect.midtop = self.top_rect.midtop
		self.bottom_rect.height = self.top_rect.height + self.dynamic_elecation

		pygame.draw.rect(surface,self.bottom_color, self.bottom_rect,border_radius = 12)
		pygame.draw.rect(surface,self.top_color, self.top_rect,border_radius = 12)
		surface.blit(self.text_surf, self.text_rect)
		self.check_click()

	def check_click(self):
		mouse_pos = pygame.mouse.get_pos()
		if self.top_rect.collidepoint(mouse_pos):
			self.top_color = '#D74B4B'
			if pygame.mouse.get_pressed()[0]:
				self.dynamic_elecation = 0
				self.pressed = True
			else:
				self.dynamic_elecation = self.elevation
				if self.pressed == True:
					self.pressed = False
		else:
			self.dynamic_elecation = self.elevation
			self.top_color = '#475F77'

def Menu() :

    playButton = Button('Play', 200, 40, (SCREEN[0] / 2 - 100, SCREEN[1] / 3 + 50), 5)
    highScoresButton = Button('High Scores', 200, 40, (SCREEN[0] / 2 - 100, SCREEN[1] / 3 + 100), 5)
    quitButton = Button('Exit', 200, 40, (SCREEN[0] / 2 - 100, SCREEN[1] / 3 + 150), 5)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if playButton.top_rect.collidepoint(event.pos):
                    main()
                elif highScoresButton.top_rect.collidepoint(event.pos):
                    loadScores()
                    showHighScores()
                elif quitButton.top_rect.collidepoint(event.pos):
                    pygame.quit()
                    sys.exit()

        surface.fill((255, 255, 255))
        playButton.draw()
        highScoresButton.draw()
        quitButton.draw()
        pygame.display.flip()
        clock.tick(FPS)

def pauseMenu() :
    continueButton = Button('Continue', 200, 40, (SCREEN[0] / 2 - 100, SCREEN[1] / 3 + 50), 5)
    quitButton = Button('Exit', 200, 40, (SCREEN[0] / 2 - 100, SCREEN[1] / 3 + 100), 5)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if continueButton.top_rect.collidepoint(event.pos):
                    return
                elif quitButton.top_rect.collidepoint(event.pos):
                    Menu()

        surface.fill((255, 255, 255))
        continueButton.draw()
        quitButton.draw()
        pygame.display.flip()
        clock.tick(FPS)

# Loading the scores from a 'scores.json' file and putting it in the global dictionary variable scores
def loadScores() :
    global scores
    try:
        with open('scores.json') as json_file:
            scores = json.load(json_file)
    except (Exception):
        print("Dosya Okurken Hata Olustu")

def showHighScores():
    scoreList = []
    scoreMessages = []
    i = 0

    for key, value in sorted(scores.items(), key=lambda item: item[1], reverse=True):
        if i > 4 :
            break
        scoreList.append([key,value])
        i += 1

    for i in range(5) :
        if i < len(scores) :
         scoreMessages.append(pygame.font.Font("res/Roboto-Regular.ttf", 45).render(scoreList[i][0] + " : " + str(scoreList[i][1])  , 1, pygame.Color("BLUE")))

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT or pygame.key.get_pressed()[K_ESCAPE]:
                Menu()

        surface.fill((255, 255, 255))

        print(scores)
        for i in range(len(scoreMessages)) :
            surface.blit(scoreMessages[i], (SCREEN[0] / 2 - 120, SCREEN[1] / 3  + 50 * i))

        pygame.display.flip()
        clock.tick(FPS)

# Taking the user name and saving the current score in a 'scores.json' file
def saveUserScore(name):
    global scores
    loadScores()
    for s in scores.keys() :
        if name == s :
            name += " (Duplicate)"
    scores[name] = SCORE
    try:
        with open('scores.json', 'w') as outfile:
            json.dump(scores, outfile)
        # for key,value in sorted(scores.items(), key=lambda item: item[1],reverse = True) :
        #     print("Key = " + key + ", Value = " + str(value))
        # # print(dict(sorted(data.items(), key=lambda item: item[1])))
    except (Exception):
        print("Dosya Yazarken Hata Olustu")

    Menu()

# For detecting if the snake has eaten the food.
def hasEaten(SnakeX,SnakeY,FoodX,FoodY):
    rect = pygame.Rect(SnakeX, SnakeY, SIZE, SIZE)
    return rect.colliderect(pygame.Rect(FoodX, FoodY, YemekSize, YemekSize))

def drawScore() :
    global surface
    global SCORE
    speed_font = pygame.font.Font(None, 30)
    speed_msg = speed_font.render("Score :  " + str(SCORE), 1, pygame.Color("Yellow"))
    surface.blit(speed_msg,(SCREEN[0] - 150,15))

def drawSpeed() :
    global surface
    global SPEED
    speed_font = pygame.font.Font(None, 30)
    speed_msg = speed_font.render("Speed :  " + "{:.2f}".format(SPEED), 1, pygame.Color("Yellow"))
    surface.blit(speed_msg,(20,15))


# Big thanks to @stackOverflow 'skrx' for providing the method for creating a textbox with pygame
def gameOver():
    pygame.mixer.Sound('res/crash.wav').play()
    time.sleep(1)
    gameOvermsg = pygame.font.Font("res/Roboto-Regular.ttf", 45).render("Game Over", 1, pygame.Color("RED"))
    scoremsg = pygame.font.Font("res/Roboto-Regular.ttf", 40).render("Score : " + str(SCORE), 1, pygame.Color("Blue"))
    saveButton = Button('Save Score', 200, 40, (SCREEN[0] / 2 - 100, SCREEN[1] / 3 + 50), 5)
    playAgainButton = Button('Play Again', 200, 40, (SCREEN[0] / 2 - 100, SCREEN[1] / 3 + 100), 5)
    quitButton = Button('Exit', 200, 40, (SCREEN[0] / 2 - 100, SCREEN[1] / 3 + 150), 5)
    base_font = pygame.font.Font(None, 32)
    user_text = ''
    input_rect = pygame.Rect(SCREEN[0] / 2 - 100, SCREEN[1] / 3, 200, 40)
    color_active = pygame.Color('lightskyblue3')
    color_passive = pygame.Color('chartreuse4')
    color = color_passive
    active = False

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if saveButton.top_rect.collidepoint(event.pos):
                    saveUserScore(user_text)
                    Menu()
                elif playAgainButton.top_rect.collidepoint(event.pos):
                    main()
                elif quitButton.top_rect.collidepoint(event.pos):
                    pygame.quit()
                    sys.exit()
                elif input_rect.collidepoint(event.pos):
                    active = ~active

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_BACKSPACE:
                    user_text = user_text[:-1]
                elif event.key == pygame.K_ESCAPE:
                    main()
                else:
                    user_text += event.unicode

        surface.fill((255, 255, 255))
        if active:
            color = color_active
        else:
            color = color_passive

        saveButton.draw()
        playAgainButton.draw()
        quitButton.draw()
        surface.blit(gameOvermsg, (SCREEN[0] / 2 - 120, SCREEN[1] / 3 - 100))
        surface.blit(scoremsg, (SCREEN[0] / 2 - 100, SCREEN[1] / 3 - 50))
        pygame.draw.rect(surface, color, input_rect)
        text_surface = base_font.render(user_text, True, (255, 255, 255))
        surface.blit(text_surface, (input_rect.x + 5, input_rect.y + 5))
        pygame.display.flip()
        clock.tick(FPS)

def main() :
    yilan = Yilan()
    yemek = Yemek()
    global  SPEED
    global surface
    global SCORE
    global SIZE

    while True:
        key = pygame.key.get_pressed()
        yilan.checkScreenSides()

        willGrow  = hasEaten(yilan.body[0][0],yilan.body[0][1],yemek.x,yemek.y)
        collosion = yilan.checkCollision()

        if (collosion):
            gameOver()
        if (willGrow):
            yilan.grow()
            SCORE += 5
            yemek.random()

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if  key[K_ESCAPE]:
                pauseMenu()
            if key[K_w]:
                SPEED += 0.2
            if key[K_s]:
                SPEED -= 0.2
            if key[K_z]:
                SIZE += 1
            if key[K_x]:
                SIZE -= 1
            if key[K_UP]:
                yilan.setDirection('UP')
            if key[K_DOWN]:
                yilan.setDirection('DOWN')
            if key[K_RIGHT]:
                yilan.setDirection('RIGHT')
            if key[K_LEFT]:
                yilan.setDirection('LEFT')

        yilan.move()
        surface.fill(WHITE)
        yilan.draw()
        yemek.draw()
        drawSpeed()
        drawScore()
        pygame.display.flip()
        clock.tick(FPS)


if __name__ == '__main__':
    Menu()