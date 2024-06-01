import asyncio
import app
import os
from app_components import clear_background
from events.input import Buttons, BUTTON_TYPES
from system.eventbus import eventbus
from system.patterndisplay.events import *
import math
from tildagonos import tildagonos, led_colours

class Image():
    def __init__(self):
        self.default_led = False

    def update(self,td):
        pass
        
    def leds(self):
        return [(0,0,0) for i in range(12)]
        
    def draw(self, ctx):
        clear_background(ctx)

class Anarcho(Image):
    def leds(self):
        return [(255,0,0) for i in range(12)]
    
    def draw(self, ctx):
        clear_background(ctx)
        # red triangle
        ctx.rgb(1, 0, 0)
        ctx.begin_path()
        ctx.move_to(120, 120)
        ctx.line_to(-120, -120)
        ctx.line_to(120, -120)
        ctx.close_path()
        ctx.fill()
        # Big A
        ctx.font_size=350
        ctx.rgb(1,1,1).move_to(int(-120/(2**.5))-20,int(120/(2**.5))+10).text("A")

        
class WaterMelon(Image):
    def leds(self):
        return [
            (0, 0, 0),
            (0, 0, 0),
            (255,255,255),
            (255,255,255),
            (0,255,20),
            (0,255,20),
            (0,255,20),
            (255,0,0),
            (255,0,0),
            (255,0,0),
            (255,0,0),
            (0, 0, 0),
        ]

    
    def draw(self, ctx):
        clear_background(ctx)
        ctx.rgb(1,1,1).rectangle(-120,-120,240,240).fill()
        r = 110
        ctx.rgb(20/255, 153/255, 84/255).arc(0, 0, r, 0.25*math.pi, 1.25 * math.pi, False).fill() #green
        ctx.rgb(1,1,1).arc(0, 0, r-15, 0.25*math.pi, 1.25 * math.pi, False).fill() #white
        ctx.rgb(228/255, 49/255, 43/255).arc(0,0, r-25, 0.25*math.pi, 1.25 * math.pi, False).fill() #red
        
        x_dot = [-50,-20,20,-40,-40,25,-15]
        y_dot = [-30,0,  30,55,-5,50,40]
        r_dot = 5
        for x,y in zip(x_dot,y_dot):
            ctx.rgb(0, 0, 0).arc(x, y, r_dot, 0, 2 * math.pi, False).fill() #black
            
class Rainbow(Image):
    # Colours from https://www.flagcolorcodes.com/pride-rainbow
    def leds(self):
        return [
            (228, 0, 0),
            (228, 0, 0),
            (255,140, 0),
            (255,140, 0),
            (255, 237, 0),
            (255, 237, 0),
            (0,128,38),
            (0,128,38),
            (36, 64, 142),
            (36, 64, 142),
            (115, 41, 130),
            (115, 41, 130),
        ]

    
    def draw(self, ctx):
        clear_background(ctx)
        ctx.rgb(228/255, 0, 0).rectangle(-120, -120, 240, 40).fill()
        ctx.rgb(1,140/255, 0).rectangle(-120, -80, 240, 40).fill()
        ctx.rgb(1, 237/255, 0).rectangle(-120, -40, 240, 40).fill()
        ctx.rgb(0, .5, 38/255).rectangle(-120, 0, 240, 40).fill()
        ctx.rgb(36/255, 64/255, 142/255).rectangle(-120, 40, 240, 40).fill()
        ctx.rgb(115/255, 41/255, 130/255).rectangle(-120, 80, 240, 40).fill()


class Trans(Image):
    def leds(self):
        return [
            (0,0,255),
            (255, 50, 50),
            (255,255,255),
            (255,255,255),
            (255, 50, 50),
            (0,0,255),
            (0,0,255),
            (255, 50, 50),
            (255,255,255),
            (255,255,255),
            (255, 50, 50),
            (0,0,255),
        ]

    
    def draw(self, ctx):
        clear_background(ctx)
        h=240/5
        ctx.rgb(91/255., 206/255., 250/255.).rectangle(-120,-120,240,h).fill()
        ctx.rgb(245/255., 169/255., 184/255.).rectangle(-120,-120+h,240,h).fill()
        ctx.rgb(1,1,1).rectangle(-120,-120+2*h,240,h).fill()
        ctx.rgb(245/255., 169/255., 184/255.).rectangle(-120,-120+3*h,240,h).fill()
        ctx.rgb(91/255., 206/255., 250/255.).rectangle(-120,-120+4*h,240,h).fill()

        
class Freedom(Image):
    def leds(self):
        return [
            (0,0,255),
            (255,255,255),
            (0,0,255),
            (0,0,255),
            (255,255,255),
            (0,0,255),
            (0,0,255),
            (255,255,255),
            (0,0,255),
            (0,0,255),
            (255,255,255),
            (0,0,255),

        ]

    
    def draw(self, ctx):
        clear_background(ctx)
        
        ctx.rgb(0/255., 94/255., 184/255.).rectangle(-120,-120,240,240).fill()
        ctx.line_width = 30
        ctx.rgb(1,1,1)
        ctx.begin_path()
        ctx.move_to(-120,-100)
        ctx.line_to(120,100)
        ctx.close_path().stroke()
        
        ctx.begin_path()
        ctx.move_to(120,-100)
        ctx.line_to(-120,100)
        ctx.close_path().stroke()
        

class Effect():
    def __init__(self):
        pass

    def animate_leds(self,colors,dt):
        return colors
    
    def draw(self,ctx):
        #TODO
        pass
    
class On(Effect):
    pass
    
class Heartbeat(Effect):
    def __init__(self):
        self.T = -1


    def animate_leds(self,colors,dt):
        tdelta = dt / 1000
        self.T += tdelta / 2 
        if self.T > 1:
            self.T -= 2
            
        scale = abs(self.T)
        
        return [tuple(int(p*scale) for p in c) for c in colors]

class Spin(Effect):
    def __init__(self):
        self.T = 0


    def animate_leds(self,colors,dt):
        tdelta = dt / 1000
        self.T += tdelta 
        if self.T > 1:
            self.T -= 1            

        scales = []
        for i in range(12):
            d = min(abs(i/12 - self.T + j) for j in range(-1,2))
            scales.append(6*max(0,1/6-d))
        
        return [tuple(int(p*s) for p in c) for s,c in zip(scales,colors)]


IMAGES = [
    Rainbow,
    Anarcho,
    Trans,
    WaterMelon,
    Freedom,
]

EFFECTS = [
    Heartbeat,
    Spin,
    On,
]

class ACApp(app.App):
    def __init__(self):
        eventbus.emit(PatternDisable())
                
        try:
            fp = open("apps/ACAB/config.txt","r")
            data = fp.read()
            fp.close()
            lines = data.split("\n")
            self.images_index = int(lines[0])
            self.effects_index = int(lines[1])
            self.shown_help = True
        except Exception: # just to be sure, also in case of bad configfiles
            self.shown_help = False
            self.images_index = 0
            self.effects_index = 0
            
        self.button_states = Buttons(self)

        self.was_paused = False
        self.max_brightness = .6

        self.images = IMAGES
        self.cur_image = self.images[self.images_index]()

        self.effects = EFFECTS
        self.cur_effect = self.effects[self.effects_index]()

        
    def update(self, delta):
        if not self.shown_help:
            for value in BUTTON_TYPES.values():
                if self.button_states.get(value):
                    # button press
                    self.write_config()
                    self.shown_help = True
                    self.button_states.clear()
                    return
            else:
                # no found
                return
        
        if self.was_paused:
            eventbus.emit(PatternDisable())
            self.was_paused = False

        
        if self.button_states.get(BUTTON_TYPES["CANCEL"]):    
            self.button_states.clear()
            # Ensure the rainbow barf can start again
            eventbus.emit(PatternEnable())
            self.was_paused = True # to stop rainbow barf when comming back online
            self.minimise()
            return
        elif self.button_states.get(BUTTON_TYPES["UP"]):
            self.max_brightness = min(1,self.max_brightness+.2)
            self.button_states.clear()
        elif self.button_states.get(BUTTON_TYPES["DOWN"]):
            self.max_brightness = max(0,self.max_brightness-.2)
            self.button_states.clear()
        elif self.button_states.get(BUTTON_TYPES["CONFIRM"]):
            self.images_index = (self.images_index+1) % len(self.images)
            self.cur_image = self.images[self.images_index]()
            self.button_states.clear()
        elif self.button_states.get(BUTTON_TYPES["RIGHT"]):
            self.effects_index = (self.effects_index+1) % len(self.effects)
            self.cur_effect = self.effects[self.effects_index]()
            self.button_states.clear()
        elif self.button_states.get(BUTTON_TYPES["LEFT"]):
            self.write_config()
                

            

        self.cur_image.update(delta)

        # Get actual colors
        colors = self.cur_image.leds()
        led_state = self.cur_effect.animate_leds(colors,delta)

        # write to leds (scaled by brightness)
        for i,c in zip(range(1,13),led_state):
            tildagonos.leds[i] = tuple(int(p*self.max_brightness) for p in c)
        tildagonos.leds.write()


    def write_config(self):
        with open("/apps/ACAB/config.txt","w") as fp:
                fp.write(str(self.images_index))
                fp.write("\n")
                fp.write(str(self.effects_index))
                fp.write("\n")


    def draw_help(self,ctx):
        clear_background(ctx)
        ctx.font_size = 15
        ctx.move_to(-20,-90).rgb(1,1,1).text("BRT+")
        ctx.move_to(-20,100).rgb(1,1,1).text("BRT-")

        ctx.move_to(0.86602540378 * 100-25,-50).rgb(1,1,1).text("Effect")
        ctx.move_to(0.86602540378 * 100-25,50).rgb(1,1,1).text("Image")

        ctx.move_to(-0.86602540378 * 100,-50).rgb(1,1,1).text("Exit")
        ctx.move_to(-0.86602540378 * 100,50).rgb(1,1,1).text("Save setup")
        

        
    def draw(self, ctx):
        if not self.shown_help:
            self.draw_help(ctx)
        else:
            self.cur_image.draw(ctx)

__app_export__ = ACApp
