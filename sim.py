import robot
import dmath as dm
import copy


class Sim:

    def __init__(self, bot):
        self.robot = bot
        self.robot_backup = copy.deepcopy(self.robot)
        self.other = None
        # History will keep track of guesses. Mostly useful for visualisation.
        self.history = []
        self.localized = False
        self.counter = 0
        self.error_tolerance = 0.5
        self.max_iterations = 100
        self.estimation_func = None

    def reset_sim(self):
        self.reset_robot()
        self.other = None
        # History will keep track of guesses. Mostly useful for visualisation.
        self.history = []
        self.localized = False
        self.counter = 0
        self.error_tolerance = 0.5
        self.max_iterations = 100
        self.estimation_func = None

    def log_prediction(self,prediction):
        self.history.append(prediction)

    def reset_robot(self):
        self.robot = copy.deepcopy(self.robot_backup)

    def print_history(self):
        for p in self.history:
            print("M:",p[0],"P:",p[1],"A:",p[2],"E:",p[3])

    def run_estimation_function(self,func):
        # Get a current (noisy) measurement of the robot's location.
        measurement = self.robot.sense()
        # Let the provided estimation function calculate a guess, using only the
        guess,self.other = func(measurement, self.other)
        self.robot.move_in_polygon()
        real_pos = self.robot.x,self.robot.y
        error_distance = dm.v2_dis(guess, real_pos)
        self.log_prediction((measurement,guess,real_pos,error_distance))
        return self.history[-1]

    def run_current_function(self):
        if self.estimation_func is None:
            raise Exception("No estimation function was provided.")
        if self.counter >= self.max_iterations:
            return None
        if not self.localized:
            self.counter += 1
            meas, guess, real, err_dis = self.run_estimation_function(self.estimation_func)
            if err_dis < self.error_tolerance:
                self.localized = True
            return meas, guess, real, err_dis

    def setup_estimation_function_test(self,func,error_tolerance=0.5,iterations=100):
        self.reset_sim()
        self.error_tolerance = error_tolerance
        self.max_iterations = iterations
        self.estimation_func = func

    def test_estimation_function_fast(self,func,tolerance=0.5,iterations=100):
        localized = False
        counter = 0
        self.reset_sim()
        if not localized and counter < iterations:
            counter += 1
            meas,guess,real,err_dis = self.run_estimation_function(func)
            if err_dis < tolerance:
                localized = True
        if localized:
            print("Localized in " + str(counter) + " steps.")
            self.print_history()
        else:
            print("Couldn't Localize")

