import math

WIDTH = 1350
HEIGHT = 629

speed = 2

car1 = Actor('noisecar1', (WIDTH/2, HEIGHT/2))

def draw():
    screen.clear()
    car1.draw()

def update():

    rad = math.radians(car1.angle)

    posx = math.sin(rad)
    posy = math.cos(rad)

    print('X SIN: ' + str(posx) + 'Y COS: ' + str(posy))



    if keyboard.up:
        car1.y -= posy * speed
        car1.x -= posx * speed
    elif keyboard.down:
        car1.y += posy * speed
        car1.x += posx * speed
    if keyboard.right:
        car1.angle -= 1
    if keyboard.left:
        car1.angle += 1