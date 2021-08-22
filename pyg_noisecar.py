from random import choice
import math
from PIL import Image
from pygame import Rect, image, transform

from enum import Enum

# Debug-Modus
debug = False

# width and height of the world
WIDTH = 1350
HEIGHT = 629

IMAGES_PATH = 'images/'

# the Cars
CAR_IMAGES = ['noisecar1', 'noisecar2']

# Race-Tracks (#name, #Start Player1, #Start Player2)
RACETRACK = [('round1', (160,350), (120,350)), ('round2', (160,350), (120,350)) , ('round3', (150,350), (130,350)), ('round4', (170,310), (150,310))]


# the relevant Colors of the Race Track

TrackGround = {
    "TRACK" : [195 , 195, 195],
    "SAND" : [255 , 202 , 24],
    "OUT" : [14 , 209 , 69],
    "START" : [0,0,0],
    "SECTION" : [0 , 168 , 243]
    }

# The State of the Game
class State(Enum):
    READY = 0
    PLAY = 1
    FINISH = 2
    EXIT = 3


class Car(Actor):

    def __init__(self, player):
        Actor.__init__(self, CAR_IMAGES[player - 1], anchor=('center', 'bottom'))

        self.max_speed = 6
        self.speed = 0
        self.damp = 0.04
        self.speed_up = 0.06
        self.speed_down = 0.3
        self.steering = 3
        self.ang = 0
        self.prevPos = self.pos
        self.player = player
        self.rec = Rect(self.topleft, (self.width, self.height))

    def update(self):

        self.rec = Rect(self.topleft, (self.width, self.height))

        if self.player == 1:
            up = keyboard.up
            down = keyboard.down
            left = keyboard.left
            right = keyboard.right
        else:
            up = keyboard.w
            down = keyboard.s
            left = keyboard.a
            right = keyboard.d

        self.ang = math.radians(self.angle)

        currentTrackColor = game.returnColor(self.x, self.y)

        if debug:
            print('currentTrackColor: ' + str(currentTrackColor))

        if currentTrackColor == TrackGround["TRACK"]:
            self.max_speed = 6
            self.damp = 0.04
        elif currentTrackColor == TrackGround["SAND"]:
            self.max_speed = 5
            self.damp = 0.06
        elif currentTrackColor == TrackGround["OUT"]:
            self.max_speed = 1.5
            self.damp = 0.2

        if self.x < WIDTH - 20 and self.x > 20 and self.y < HEIGHT - 20 and self.y > 20:
            if left and (self.speed != 0 or down or up):
                self.angle += self.steering
            if right and (self.speed != 0 or down or up):
                self.angle -= self.steering
            if up:
                if self.speed == 0:
                   self.speed += self.speed_up
                elif self.speed < 0:
                   self.speed += self.speed_down
                elif self.speed > 0 and self.speed < self.max_speed:
                   self.speed *= (1 + self.speed_up)
                else:
                    self.speed -= self.speed_down
            elif down:
                if self.speed == 0:
                   self.speed -= self.speed_up
                elif self.speed > 0:
                   self.speed -= self.speed_down
                elif self.speed < 0 and self.speed > -self.max_speed:
                   self.speed *= (1 + self.speed_up)
                else:
                    self.speed += self.speed_down
            else:
                self.speed *= (1 - self.damp)
                if abs(self.speed) < self.speed_up:
                  self.speed = 0
            self.prevPos = self.pos
            self.pos = (self.x + -math.sin(self.ang) * self.speed), (self.y + -math.cos(self.ang) * self.speed)
        else:
            self.speed = 0
            self.pos = self.prevPos


    def draw(self):
        super().draw()

class Game():
    def __init__(self):
        self.selectTrack = 1
        self.image = Image
        self.image_rgb = Image
        self.trackTump = transform.scale(image.load(IMAGES_PATH +  RACETRACK[self.selectTrack - 1][0] + '.png'), (300,140))
        self.player1 = Car(1)
        self.player2 = Car(2)
        self.state = State.READY
        self.keyPressed = True

    def draw(self):

        if game.state == State.READY:
            screen.blit( 'noisecarintro' , (0, 0))
            screen.blit( self.trackTump, (520,225))
            if keyboard.right and self.keyPressed:
                self.levelSelect(True)
                self.keyPressed = False
            elif keyboard.left and self.keyPressed:
                self.levelSelect(False)
                self.keyPressed = False
            elif not keyboard.right and not keyboard.left:
                self.keyPressed = True

        if game.state == State.PLAY:
            screen.blit( RACETRACK[self.selectTrack - 1][0] , (0, 0))
            self.player1.draw()
            self.player2.draw()


            screen.draw.rect(self.player1.rec, color="orange")
            screen.draw.rect(self.player2.rec, color="red")

    def update(self):
        if keyboard.space and game.state == State.READY:
            game.state = State.PLAY
            self.image = Image.open(IMAGES_PATH + RACETRACK[game.selectTrack - 1][0] + '.png')
            self.image_rgb = self.image.convert('RGB')
            game.player1.pos = RACETRACK[game.selectTrack - 1][1]
            game.player2.pos = RACETRACK[game.selectTrack - 1][2]

        if game.state == State.PLAY:
            self.player1.update()
            self.player2.update()
            self.checkCollision()

    def levelSelect(self, isForward):
        if isForward:
            if self.selectTrack < len(RACETRACK):
                self.selectTrack +=1
            else:
                self.selectTrack = 1
        elif self.selectTrack > 1:
            self.selectTrack -= 1
        else:
            self.selectTrack = len(RACETRACK)
        self.trackTump = transform.scale(image.load(IMAGES_PATH +  RACETRACK[self.selectTrack - 1][0] + '.png'), (300,140))

    def returnColor(self,x,y):
        color = list(self.image_rgb.getpixel((x, y)))
        if debug:
            print ('Pixelkoordinaten: %3s %3s Rot: %3s Gruen: %3s Blau: %3s' % (x,y,color[0],color[1],color[2]))
        return color

    def checkCollision(self):
        if self.player1.colliderect(self.player2):
            self.player1.speed = 0
            self.player2.speed = 0

        # Todo: das Zusammenstossen der Autos soll realer sein.
        #if Rect.collidepoint(self.player1.rec, self.player2.midtop):
        #    print('Auuuuua!')
        #else:
        #    print('Nix!')
        #print(str(self.player1.distance_to(self.player2)))
        #print(str(self.player1.angle_to(self.player2)))

# draws the current frame
def draw():
    screen.clear()
    game.draw()

    if debug:
        screen.draw.text("speed: " + str(game.player1.speed),(50, 80))
        screen.draw.text(str(math.radians(game.player1.angle)),(50, 5))
        screen.draw.text("x sin: " + str(math.sin(math.radians(game.player1.angle))),(50, 20))
        screen.draw.text("y cos: " + str(math.cos(math.radians(game.player1.angle))),(50, 35))
        screen.draw.text("x sin * 2: " + str(math.sin(math.radians(game.player1.angle)) * 2),(50, 50))
        screen.draw.text("y cos * 2: " + str(math.cos(math.radians(game.player1.angle)) * 2),(50, 65))


# Pygame Zero update function
def update():
    game.update()

game = Game()
