import pyglet
import math
from pyglet.window import key
import sim
import numpy as np
import dmath as dm

def center_image(image):
    """Sets an image's anchor point to its center"""
    image.anchor_x = image.width // 2
    image.anchor_y = image.height // 2


def createGraphics():
    pyglet.resource.path = ['./resources']
    pyglet.resource.reindex()
    bot_img = pyglet.resource.image("robot.png")
    prediction_img = pyglet.resource.image("prediction.png")
    measurement_img = pyglet.resource.image("measurement.png")
    bot_img.anchor_x = 68
    bot_img.anchor_y = bot_img.height // 2
    prediction_img.anchor_x = 68
    prediction_img.anchor_y = prediction_img.height // 2
    center_image(measurement_img)
    return bot_img,prediction_img,measurement_img



class Visualisation:
    def __init__(self, simulation: sim.Sim, updateInt = 1.0, ):
        """

        :type simulation: sim.Sim
        """
        self.sim = simulation
        self.updateInt = updateInt
        self.coord_scale = 1.0
        self.transform_matrix = np.identity(3)

        self.window = pyglet.window.Window(1000, 600, "Localization Visualisation", True)
        self.imgBot, self.imgPred, self.imgMeas = createGraphics()
        self.bot = pyglet.sprite.Sprite(self.imgBot)
        pyglet.gl.glClearColor(0.5, 0.8, .9, 1)
        # center of window
        self.center = [self.window.width / 2.0, self.window.height / 2.0]
        self.localizedLabel = pyglet.text.Label('Not Localized',
                                                font_name='Times New Roman',
                                                font_size=24,
                                                x=self.center[0], y=self.window.height-50,
                                                anchor_x='center', anchor_y='center')
        self.pauseLabel = pyglet.text.Label('Paused.\nPress Spacebar',
                                                font_name='Times New Roman',
                                                font_size=40,
                                                x=self.center[0], y=self.center[1],
                                                anchor_x='center', anchor_y='center')
        self.paused = True
        self.window.on_key_press = self.on_key_press
        self.window.on_draw = self.on_draw

        self.prediction = pyglet.sprite.Sprite(self.imgPred)
        self.prediction.scale = 2.0
        self.bot.scale = 1.0
        self.transform_matrix = dm.translation_matrix(self.center[0],self.center[1])@dm.scale_matrix(4.0,4.0)
        self.bot.position = dm.tmat(self.transform_matrix,(0,0))
        self.prediction.position = dm.tmat(self.transform_matrix, (-10, -10))
    def on_key_press(self,symbol, modifiers):
        if symbol == key.SPACE:
            self.paused = False if self.paused else True

    def on_draw(self):
        self.window.clear()
        self.bot.draw()
        self.prediction.draw()
        self.localizedLabel.draw()
        if self.paused:
            self.pauseLabel.draw()

    def run(self):
        pyglet.clock.schedule_interval(self.on_update, self.updateInt)
        pyglet.app.run()

    def on_update(self, dt):
        if self.paused:
            return
        new_state = self.sim.run_current_function()
        if new_state is None:
            pass
        else:
            meas, guess, real, err_dis = new_state
            self.prediction.position = dm.tmat(self.transform_matrix,guess)
            if self.sim.localized:
                self.set_localized(self.sim.counter)
        self.update_graphics()

    def update_graphics(self):
        pos = self.sim.robot.x, self.sim.robot.y
        self.bot.position = dm.tmat(self.transform_matrix,pos)
        self.bot.rotation = math.degrees(-self.sim.robot.heading)



    def set_localized(self,steps):
        self.localizedLabel.text = "You got it right! It took you "+ str(steps)+ "\nsteps to localize."