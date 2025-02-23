import pyxel
from enum import Enum


class App:


    def __init__(self):
        pyxel.init(128, 120, title="Motivational Claw Game")
        pyxel.load("claw.pyxres")
        self.claw = Claw()

        pyxel.playm(0, loop=True)
        pyxel.run(self.update, self.draw)

    def update(self):
        if pyxel.btnp(pyxel.KEY_Q):
            pyxel.quit()
        self.claw.update()

    def draw(self):
        pyxel.cls(12)
        pyxel.camera()

        # backdrop
        pyxel.bltm(0, 30, 0, 0, 30, 128, 78)
        # # machine overlay
        pyxel.bltm(0, 0, 0, 0, 0, 128, 30)
        # # draw claw
        self.claw.draw(True)

        pyxel.bltm(0, 108, 0, 0, 108, 128, 20)


class Claw:
    class State(Enum):
        DEFAULT = 1
        DESCENDING = 3
        GRABBING = 4
        ASCENDING = 5
        DISPLAYING_MESSAGE = 6
    def __init__(self):
        self.x = 64
        self.y = 20

        self.arm_length_min=8
        self.arm_length_max=40

        self.arm_length = self.arm_length_min
        self.state = self.State.DEFAULT

        self.grab_timer = 0

    def draw(self, debug = False):

        self.draw_mount()

        # draw wheel
        wheel_x = 8 * ((self.x // 4) % 2)
        wheel_y = 24 + 8*((self.x // 8) % 2)
        pyxel.blt(self.x, 20, 0, wheel_x, wheel_y, 8, 8, 14)

        self.draw_arm()
        self.draw_claw()

        if(debug):
            pyxel.text(4, 4, f"X: {self.x} Y: {self.y}", 0)

            pyxel.line(0, self.y, 140, self.y, 3)
            pyxel.line(self.x, 0, self.x, 120, 7)
            
            pyxel.text(4, 10, f"State: {self.state}", 0)
            pyxel.text(4, 16, f"Arm Length: {self.arm_length}", 0)

    
    def draw_mount(self):
        pyxel.blt(self.x - 8, 24, 0, 48, 0, 16, 8, 14)

    def draw_arm(self):
        start_y=self.y+12
        # drawLine_y(start_y)
        end_y=self.arm_length+start_y
        # drawLine_y(end_y,9)
        arm_x=self.x -8
        arm_y=self.arm_length-8
        
        # pyxel.blt(arm_x, arm_y,0, 48, 8,16,8, 14) 
        pyxel.blt(self.x-8, 32,0,48,8, 16, 8, 14)

    def draw_claw(self):
        claw_y = self.y +12
        if self.state == Claw.State.GRABBING:    
            pyxel.blt(self.x-8, claw_y + self.arm_length,0,32,0, 16, 16, 14)
        else:
            pyxel.blt(self.x-8, claw_y + self.arm_length,0,32,16, 16, 16, 14)

    def update(self):  

        if self.state == Claw.State.DEFAULT:
            self.update_default()
        elif self.state == Claw.State.DESCENDING:
            self.update_descending()
        elif self.state == Claw.State.GRABBING:
            self.update_grabbing()
        elif self.state == Claw.State.ASCENDING:
            self.update_ascending()

        if pyxel.btn(pyxel.KEY_DOWN):
            self.arm_length = min(self.arm_length + 2, self.arm_length_max)              
        if pyxel.btn(pyxel.KEY_UP):
            self.arm_length = max(self.arm_length - 2, self.arm_length_min)   

    def update_default(self):
        if pyxel.btn(pyxel.KEY_LEFT):
            self.x = max(self.x - 2, 0)
        if pyxel.btn(pyxel.KEY_RIGHT):
            self.x = min(self.x + 2, pyxel.width - 16)   
        if pyxel.btn(pyxel.KEY_SPACE):
            self.state = Claw.State.DESCENDING   

    def update_descending(self):    
        self.arm_length += 1 
        if self.arm_length > self.arm_length_max:
            self.grab_timer = 15
            self.state = Claw.State.GRABBING

    def update_grabbing(self):
        self.grab_timer -= 1
        if self.grab_timer == 0:
            self.state = Claw.State.ASCENDING

    def update_ascending(self):
        self.arm_length -=1
        if self.arm_length == self.arm_length_min:
            self.state = Claw.State.DEFAULT

def drawLine_y(y, col = 8):
    pyxel.line(0, y, 128, y, col)

App()
