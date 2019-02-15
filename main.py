from robot import Robot
from math import *
import turtle
import numpy as np
import random
import pyglet
import math
from pyglet.window import key
def distance_between(point1, point2):
    """Computes distance between point1 and point2. Points are (x, y) pairs."""
    x1, y1 = point1
    x2, y2 = point2
    return sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)

def center_image(image):
    """Sets an image's anchor point to its center"""
    image.anchor_x = image.width // 2
    image.anchor_y = image.height // 2


dis_tolerance = 0.02
def estimate_next_pos(measurement, particles):
    #simple random guess around the last measurement.
    estimate = (measurement[0] + random.uniform(-5.0,5.0)
                ,measurement[1]+random.uniform(-5.0,5.0))
    return estimate, particles

def createGraphics(mb):
    pyglet.resource.path = ['./resources']
    pyglet.resource.reindex()
    botImg = pyglet.resource.image("robot.png")
    predictionImg = pyglet.resource.image("prediction.png")
    measurementImg = pyglet.resource.image("measurement.png")
    center_image(botImg)
    center_image(predictionImg)
    center_image(measurementImg)
    botSprite = pyglet.sprite.Sprite(botImg,batch=mb)
    predictionSprite = pyglet.sprite.Sprite(predictionImg,batch=mb)
    measurementSprite = pyglet.sprite.Sprite(measurementImg,batch=mb)
    tscale = 1.0
    botSprite.scale = tscale
    predictionSprite.scale = tscale
    measurementSprite.scale = tscale


    return (botSprite,predictionSprite,measurementSprite)

#create window
window = pyglet.window.Window()
coordScale = 2.0
pyglet.gl.glClearColor(0.5,0.8,.9,1)
#center of window
center = [window.width/2.0,window.height/2.0]
center[0]/=coordScale
center[1]/=coordScale
localized = False
counter = 0

# Create the needed sprites
main_batch = pyglet.graphics.Batch()
bot, pred, meas = createGraphics(main_batch)
localizedLabel = pyglet.text.Label('Not Localized',
                              font_name='Times New Roman',
                              font_size=24,
                              x=window.width // 2, y=window.height // 4,
                              anchor_x='center', anchor_y='center')
paused = True
# Create the Robot class, which handles movement and noise, etc.
# To draw the bot sprite, we will copy the location/orientation from the robot object.
startPos = [9.84595717195,-3.82584680823]
test_target = Robot(startPos[0],startPos[1], 3.08457233661, 2*pi /-5, 3.08457233661 ,8, 20)
test_target.set_noise(0.0, 0.0, .05)
OTHER = None

@window.event
def on_key_press(symbol, modifiers):
    global paused
    if (symbol == key.SPACE):
        paused = False if paused else True



@window.event
def on_draw():
    global localized
    window.clear()

    bot.draw()
    pred.draw()
    meas.draw()
    #meas.visible = False

    localizedLabel.draw()

totalTime = 0.0
def update(dt):
    global totalTime
    global counter, coordScale
    global localized
    global test_target
    global OTHER
    global bot, pred, meas
    global dis_tolerance
    measurement = None
    position_guess = None
    if not paused:
        totalTime += dt
        counter += 1
        distance_tolerance = dis_tolerance * test_target.distance
        if not localized and counter <= 1000:
            measurement = test_target.sense()
            position_guess, OTHER = estimate_next_pos(measurement,OTHER)
            test_target.move_in_polygon()
            true_position = (test_target.x, test_target.y)
            error = distance_between(position_guess, true_position)
            print("error: ", error)
            print("threshold: ", distance_tolerance)
            if error <= distance_tolerance:
                localizedLabel.text = "You got it right! It took you "+ str(counter)+ " steps to localize."
                localized = True
            if counter == 1000:
                print("Sorry, it took you too many steps to localize the target.")
            #meas.visible = True
            pred.visible = True
            #.opacity =sin(totalTime)*50.0+50.0
            #meas.set_position(center[0] + measurement[0] * coordScale, measurement[1] * coordScale + center[1])
            pred.set_position(center[0] + position_guess[0] * coordScale, position_guess[1] * coordScale + center[1])
    bot.set_position(center[0] + test_target.x * coordScale, test_target.y * coordScale + center[1])
    bot.rotation = math.degrees(-test_target.heading)


pyglet.clock.schedule_interval(update, 1/10.0)
pyglet.app.run()



{'test_case': 7,
                      'target_x': -17.2113204789,
                      'target_y': 10.5496426749,
                      'target_heading': -2.07830482038,
                      'target_period': 3,
                      'target_speed': 4.58689282387,
                      'target_line_length': 10,
                      'hunter_x': -7.95068213364,
                      'hunter_y': -4.00088251391,
                      'hunter_heading': 0.281505756944,
                      'random_move': 20},

{'test_case': 9,
                      'target_x': 13.6383033581,
                      'target_y': -19.2494482213,
                      'target_heading': 3.08457233661,
                      'target_period': -5,
                      'target_speed': 3.08457233661,
                      'target_line_length': 8,
                      'hunter_x': -0.414540470517,
                      'hunter_y': 13.2698415309,
                      'hunter_heading': -2.21974457597,
                      'random_move': 20},

GLOBAL_PARAMETERS = [None,
                     {'test_case': 1,
                      'target_x': 9.84595717195,
                      'target_y': -3.82584680823,
                      'target_heading': 1.95598927002,
                      'target_period': -6,
                      'target_speed': 2.23288537085,
                      'target_line_length': 12,
                      'hunter_x': -18.9289073476,
                      'hunter_y': 18.7870153895,
                      'hunter_heading': -1.94407132569,
                      'random_move': 20},

                    {'test_case': 2,
                     'target_x': -7.30880841813,
                     'target_y': -7.5606752408,
                     'target_heading': 2.69362855848,
                     'target_period': 3,
                     'target_speed': 1.51140830722,
                     'target_line_length': 2,
                     'hunter_x': -5.72203926243,
                     'hunter_y': 0.516750503883,
                     'hunter_heading': 2.93680309891,
                     'random_move': 20 },

                     {'test_case': 3,
                      'target_x': -8.23729263767,
                      'target_y': 0.167449172934,
                      'target_heading': -2.90891604491,
                      'target_period': -8,
                      'target_speed': 2.86280919028,
                      'target_line_length': 5,
                      'hunter_x': -1.26626321675,
                      'hunter_y': 10.2766202621,
                      'hunter_heading': -2.63089786461,
                      'random_move': 20},
                     {'test_case': 4,
                      'target_x': -2.18967022691,
                      'target_y': 0.255925949831,
                      'target_heading': 2.69251137563,
                      'target_period': -12,
                      'target_speed': 2.74140955105,
                      'target_line_length': 15,
                      'hunter_x': 4.07484976298,
                      'hunter_y': -10.5384658671,
                      'hunter_heading': 2.73294117637,
                      'random_move': 20},
                     {'test_case': 5,
                      'target_x': 0.363231634197,
                      'target_y': 15.3363820727,
                      'target_heading': 1.00648485361,
                      'target_period': 7,
                      'target_speed': 4.01304863745,
                      'target_line_length': 15,
                      'hunter_x': -19.6386687235,
                      'hunter_y': -13.6078079345,
                      'hunter_heading': -2.18960549765,
                      'random_move': 20},
                     {'test_case': 6,
                      'target_x': 19.8033444747,
                      'target_y': 15.8607456499,
                      'target_heading': 2.91674681677,
                      'target_period': 10,
                      'target_speed': 4.11574616586,
                      'target_line_length': 1,
                      'hunter_x': -13.483627167,
                      'hunter_y': 7.60284054436,
                      'hunter_heading': 2.45511184918,
                      'random_move': 20},
                     {'test_case': 7,
                      'target_x': -17.2113204789,
                      'target_y': 10.5496426749,
                      'target_heading': -2.07830482038,
                      'target_period': 3,
                      'target_speed': 4.58689282387,
                      'target_line_length': 10,
                      'hunter_x': -7.95068213364,
                      'hunter_y': -4.00088251391,
                      'hunter_heading': 0.281505756944,
                      'random_move': 20},
                     {'test_case': 8,
                      'target_x': 10.5639252231,
                      'target_y': 13.9095062695,
                      'target_heading': -2.92543870157,
                      'target_period': 10,
                      'target_speed': 2.2648280036,
                      'target_line_length': 11,
                      'hunter_x': 4.8678066293,
                      'hunter_y': 4.61870594164,
                      'hunter_heading': 0.356679261444,
                      'random_move': 20},
                     {'test_case': 9,
                      'target_x': 13.6383033581,
                      'target_y': -19.2494482213,
                      'target_heading': 3.08457233661,
                      'target_period': -5,
                      'target_speed': 4.8813691359,
                      'target_line_length': 8,
                      'hunter_x': -0.414540470517,
                      'hunter_y': 13.2698415309,
                      'hunter_heading': -2.21974457597,
                      'random_move': 20},
                     {'test_case': 10,
                      'target_x': -2.97944715844,
                      'target_y': -18.7085807377,
                      'target_heading': 2.80820284661,
                      'target_period': 8,
                      'target_speed': 3.67540398247,
                      'target_line_length': 8,
                      'hunter_x': 16.7631157868,
                      'hunter_y': 8.8386686632,
                      'hunter_heading': -2.91906838766,
                      'random_move': 20}]