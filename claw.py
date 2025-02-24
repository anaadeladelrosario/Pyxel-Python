import pyxel
from enum import Enum
SCREEN_WIDTH = 128
SCREEN_HEIGHT = 120

class App:
    class State(Enum):
        GAME = 0
        DISPLAYING_MESSAGE = 1

    def __init__(self):
        pyxel.init(SCREEN_WIDTH, SCREEN_HEIGHT, title="Motivational Claw Game")
        pyxel.load("claw.pyxres")
        self.init()
        pyxel.playm(0, loop=True)
        pyxel.run(self.update, self.draw)

    def init(self):
        self.claw = Claw()
        self.state = App.State.GAME
  

    def update(self):
        if pyxel.btnp(pyxel.KEY_Q):
            pyxel.quit()

        if self.state == App.State.GAME:            
            self.claw.update()
            if self.claw.state == Claw.State.FINISHED:
                self.state = App.State.DISPLAYING_MESSAGE
        elif self.state == App.State.DISPLAYING_MESSAGE:
            pass
            

    def draw(self):
        if self.state == App.State.GAME:
            self.draw_game()
        elif self.state == App.State.DISPLAYING_MESSAGE:
            self.draw_message()

    def draw_game(self):
        # backdrop
        pyxel.bltm(0, 30, 0, 0, 30, SCREEN_WIDTH, 78)
            # # machine overlay
        pyxel.bltm(0, 0, 0, 0, 0, SCREEN_WIDTH, 30)
        self.draw_background_messages()
        self.claw.draw(True)
        pyxel.bltm(0, 108, 0, 0, 108, SCREEN_WIDTH, 20)

    def draw_message(self):
        pyxel.bltm(0,0,1,0,0,SCREEN_WIDTH,SCREEN_HEIGHT)

    def draw_background_messages(self):
        def draw_scroll(x, height, col):
            floor = 108
            pyxel.rect(x, floor-height, 2, height, col)
        counter = 0
        # while counter < SCREEN_WIDTH
        #   draw a rolled up message at the counter X position at the bottom of the prize machine
        #   add a random number to the counter
        draw_scroll(6, 10,13)

        pass

class Claw:
    class State(Enum):
        DEFAULT = 1
        DESCENDING = 3
        GRABBING = 4
        ASCENDING = 5
        FINISHED = 6
    def __init__(self):
        self.x = 64
        self.y = 20

        self.arm_length_min=8
        self.arm_length_max=60 

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

            # pyxel.line(0, self.y, 140, self.y, 3)
            # pyxel.line(self.x, 0, self.x, 120, 7)
            
            pyxel.text(4, 10, f"State: {self.state}", 0)
            pyxel.text(4, 16, f"Arm Length: {self.arm_length}", 0)

    
    def draw_mount(self):
        pyxel.blt(self.x - 8, 24, 0, 48, 0, 16, 8, 14)

    def draw_arm(self):
        start_y = self.y + 12
        # drawLine_y(start_y)
        end_y =  self.arm_length + start_y
        # drawLine_y(end_y,9)
        arm_x=self.x -8
        arm_y=self.arm_length-8
        
        # pyxel.blt(arm_x, arm_y,0, 48, 8,16,8, 14)   
        if self.state == Claw.State.DEFAULT:
         pyxel.blt(self.x-8, 32,0,48,8, 16, 8, 14)
        elif self.state == Claw.State.DESCENDING or Claw.State.GRABBING:
            for i in range (self.arm_length):
             pyxel.blt(self.x-8, i + start_y - ( i % 8) ,0,48,8, 16, 8, 14)
              
        elif self.state == Claw.State.ASCENDING:
            for i in range (self.arm_length):
                pyxel.blt(self.x-8, i + start_y -( i % 8) , 0, 48, 8, 16, 8, 14)
  
    def draw_claw(self):
        claw_y = self.y +12
        if self.state == Claw.State.GRABBING or self.state == Claw.State.ASCENDING:    
            pyxel.blt(self.x-8, claw_y + self.arm_length,0,32,32, 16, 24, 14)
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
            self.grab_timer = 25
            self.state = Claw.State.GRABBING

    def update_grabbing(self):
        self.grab_timer -= 1
        if self.grab_timer == 0:
            self.state = Claw.State.ASCENDING

    def update_ascending(self):
        self.arm_length -=1
        if self.arm_length == self.arm_length_min:
            self.state = Claw.State.FINISHED

def drawLine_y(y, col = 8):
    pyxel.line(0, y, SCREEN_WIDTH, y, col)

App()
