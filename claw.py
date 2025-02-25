import pyxel
import random
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
        self.message = Message()

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
        pyxel.cls(0)
        pyxel.camera()
        # backdrop
        pyxel.bltm(0, 30, 0, 0, 30, SCREEN_WIDTH, 78)
        # # machine overlay
        pyxel.bltm(0, 0, 0, 0, 0, SCREEN_WIDTH, 30)
        self.draw_background_messages()
        self.claw.draw()
        pyxel.bltm(0, 108, 0, 0, 108, SCREEN_WIDTH, 20)

    def draw_message(self):
        pyxel.bltm(0,0,1,0,0,SCREEN_WIDTH,SCREEN_HEIGHT)
        self.message.update()

   
    def randomize_background_messages(self, x, y, rotation, size):
        random.seed(3)
        for i in range(0,SCREEN_WIDTH, 6):
            angle = random.randint(-15,rotation)
            scale = random.random()*size
            pyxel.blt(i,100, 0, x , y, 8,8,14, scale=scale+0.9, rotate= angle)

    def draw_background_messages(self): 
        self.randomize_background_messages(0,72, 45, 1.4)
        self.randomize_background_messages(8,64, 25, 1.0)
        self.randomize_background_messages(0,64, -15, 1.9)
        

class Message:
    def __init__(self):
        self.messages  = [
            "Believe in yourself!",
            "You can achieve anything!",
            "Stay positive, work hard, make it happen!",
            "Dream big and dare to fail!",
            "The only limit is your mind."
            ]

        self.message = self.messages[random.randint(0,4)]
       
    def split_message(self, text):
        lines = []
        max_width_chars = 24

        words = text.split(' ')
        current_line = ""
    
        for word in words:
            if len(current_line + word) <= max_width_chars:
                current_line += word + ' '
            else:
                lines.append(current_line.strip())
                current_line = word + ' '
        if current_line:
            lines.append(current_line.strip())
        return lines

    def update(self):
        splited_message = self.split_message(self.message)
        y_pos = 40
        for i, line in enumerate(splited_message):
            pyxel.text(24, i + y_pos, line, 0)
            y_pos += 8
            

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
            pyxel.line(0, self.y, 140, self.y, 3)
            pyxel.line(self.x, 0, self.x, 120, 7)
            pyxel.text(4, 10, f"State: {self.state}", 0)
            pyxel.text(4, 16, f"Arm Length: {self.arm_length}", 0)
    
    def draw_mount(self):
        pyxel.blt(self.x - 8, 24, 0, 48, 0, 16, 8, 14)

    def draw_arm(self):
        arm_y = self.y + 12
        arm_x=self.x -8

        if self.state == Claw.State.DEFAULT:
         pyxel.blt(self.x-8, 32,0,48,8, 16, 8, 14)
        elif self.state == Claw.State.DESCENDING or Claw.State.GRABBING or self.state == Claw.State.ASCENDING:
            for i in range (self.arm_length):
             pyxel.blt(arm_x, i + arm_y - ( i % 8) ,0,48,8, 16, 8, 14)
  
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
