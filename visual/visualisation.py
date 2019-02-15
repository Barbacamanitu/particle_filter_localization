import pyglet
import math
from pyglet.window import key

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



class Visualisation():
    def __init__(self,coord_scale=1.0):
        self.coord_scale = coord_scale
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
        self.paused = False
        self.window.on_key_press = self.on_key_press
        self.window.on_draw = self.on_draw
        self.measurements = []
        self.mI = 0
        self.prediction = pyglet.sprite.Sprite(self.imgPred)
        self.prediction.scale = 2.0
        self.bot.scale = 1.0
    def on_key_press(self,symbol, modifiers):
        if symbol == key.SPACE:
            self.paused = False if self.paused else True

    def on_draw(self):

        self.window.clear()
        # meas.draw()
        # meas.visible = False
        self.bot.draw()
        self.prediction.draw()
        self.localizedLabel.draw()

    def run(self):
        pyglet.app.run()

    def fix_coords(self,coords):
        x,y = coords
        x *= self.coord_scale
        y *= self.coord_scale

        return (self.center[0]+ x,self.center[1]+ y)

    def update_robot(self,bot):
        self.bot.position = self.fix_coords((bot.x,bot.y))
        self.bot.rotation = math.degrees(-bot.heading)

    def on_update_func(self,func,interval):
        pyglet.clock.schedule_interval(func,interval)


    def add_measurement(self,m):
        max_meas = 100
        return
        if len(self.measurements) < max_meas:
            meas = pyglet.sprite.Sprite(img=self.imgMeas,batch=self.mbatch)
            self.measurements.append(meas)
        self.measurements[self.mI].position = m[0] + self.center[0],m[1] + self.center[1]
        self.mI = (self.mI + 1) % min(max_meas,len(self.measurements))



    def add_prediction(self,p):
        self.prediction.position = self.fix_coords(p)

    def set_localized(self,steps):
        self.localizedLabel.text = "You got it right! It took you "+ str(steps)+ "\nsteps to localize."