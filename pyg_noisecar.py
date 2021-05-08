import math

WIDTH = 1350
HEIGHT = 629

speed = 0.2
max_speed = 6

car1 = Actor('noisecar1', (WIDTH/2, HEIGHT/2))

prevPos = car1.pos

carDOWN = False
carUP = False

def draw():
    screen.clear()
    car1.draw()

def update():

    global prevPos, speed, carDOWN, carUP

    rad = math.radians(car1.angle)

    posx = math.sin(rad)
    posy = math.cos(rad)

    print('Pos: ' + str(car1.pos))

    if car1.x < WIDTH - 40 and car1.x > 40 and car1.y < HEIGHT - 40 and car1.y > 40:

        prevPos = car1.pos

        if keyboard.up:
            if speed < max_speed:
                speed = speed * 1.2
            car1.y -= posy * speed
            car1.x -= posx * speed
            carUP = True
            carDOWN = False
        elif keyboard.down:
            if speed < max_speed:
                speed = speed * 1.2
            car1.y += posy * speed
            car1.x += posx * speed
            carDOWN = True
            carUP = False

        else:
            if speed > 0.2:
                speed = speed * 0.98
                if carUP:
                    car1.y -= posy * speed
                    car1.x -= posx * speed
                elif carDOWN:
                    car1.y += posy * speed
                    car1.x += posx * speed
    else:
        car1.pos = prevPos

    if speed > 0.2:
        if keyboard.right:
            car1.angle -= 1
        if keyboard.left:
            car1.angle += 1






