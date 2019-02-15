import sim
import robot
from math import *
import random
import visual.visualisation as vz


def estimate_next_pos(measurement,other):
    estimate = (measurement[0] + random.uniform(-5.0, 5.0)
                , measurement[1] + random.uniform(-5.0, 5.0))
    return estimate, other


bot = robot.Robot(9.84595717195,-3.82584680823, 3.08457233661, 2*pi /-5, 3.08457233661 , 8, 20)
bot.set_noise(0.0, 0.0, .05)
s = sim.Sim(bot)
s.setup_estimation_function_test(estimate_next_pos,0.5,1000)
v = vz.Visualisation(s,1.0/10.0)
v.run()
