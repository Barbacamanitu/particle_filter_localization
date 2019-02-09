from bot.robot import Robot
from math import *
import turtle

def distance_between(point1, point2):
    """Computes distance between point1 and point2. Points are (x, y) pairs."""
    x1, y1 = point1
    x2, y2 = point2
    return sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)


def add_measurement(measurement,history):
    if history is None:
        history = []
    history.append(measurement)
    return history



def estimate_next_pos(measurement,history):
    estimate = measurement
    history = add_measurement(measurement,history)
    return (5,5),history


def demo_grading_vis(estimate_next_pos_fcn, target_bot, history = None):
    localized = False
    distance_tolerance = 0.02 * target_bot.distance
    ctr = 0
    # if you haven't localized the target bot, make a guess about the next
    # position, then we move the bot and compare your guess to the true
    # next position. When you are close enough, we stop checking.
    #For Visualization
    #You need to run this locally to use the turtle module
    window = turtle.Screen()
    window.bgcolor('white')
    size_multiplier= 3.0  #change Size of animation
    broken_robot = turtle.Turtle()
    broken_robot.shape('turtle')
    broken_robot.color('green')
    broken_robot.resizemode('user')
    broken_robot.shapesize(0.3, 0.3, 0.3)
    measured_broken_robot = turtle.Turtle()
    measured_broken_robot.shape('circle')
    measured_broken_robot.color('red')
    measured_broken_robot.resizemode('user')
    measured_broken_robot.shapesize(0.3, 0.3, 0.3)
    prediction = turtle.Turtle()
    prediction.shape('arrow')
    prediction.color('blue')
    prediction.resizemode('user')
    prediction.shapesize(0.3, 0.3, 0.3)
    prediction.penup()
    broken_robot.penup()
    measured_broken_robot.penup()
    #End of Visualization
    while not localized and ctr <= 1000:
        ctr += 1
        measurement = target_bot.sense()
        position_guess, history = estimate_next_pos_fcn(measurement, history)
        target_bot.move_in_polygon()
        true_position = (target_bot.x, target_bot.y)
        error = distance_between(position_guess, true_position)
        print("error: ", error)
        print("threshold: ", distance_tolerance)
        if error <= distance_tolerance:
            print ("You got it right! It took you ", ctr, " steps to localize.")
            localized = True
        if ctr == 1000:
            print ("Sorry, it took you too many steps to localize the target.")
        #More Visualization
        measured_broken_robot.setheading(target_bot.heading*180/pi)
        measured_broken_robot.goto(measurement[0]*size_multiplier, measurement[1]*size_multiplier-200)
        measured_broken_robot.stamp()
        broken_robot.setheading(target_bot.heading*180/pi)
        broken_robot.goto(target_bot.x*size_multiplier, target_bot.y*size_multiplier-200)
        broken_robot.stamp()
        prediction.setheading(target_bot.heading*180/pi)
        prediction.goto(position_guess[0]*size_multiplier, position_guess[1]*size_multiplier-200)
        prediction.stamp()
        #End of Visualization
    return localized
#
test_target = Robot(0.5, -0.5, 3.08457233661, 2*pi /-5, 3.08457233661 ,8, 20)
mnoise = .05 * test_target.distance
test_target.set_noise(0.0, 0.0, .05)
demo_grading_vis(estimate_next_pos,test_target)

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