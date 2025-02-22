import pyxel


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
        self.claw.draw()

        pyxel.bltm(0, 108, 0, 0, 108, 128, 20)




class Claw:
    def __init__(self):
        self.x = 64
        self.y = 20

    def draw(self, debug = False):

        self.draw_mount()

        # draw wheel
        wheel_x = 8 * ((self.x // 4) % 2)
        wheel_y = 24 + 8*((self.x // 8) % 2)
        pyxel.blt(self.x, 20, 0, wheel_x, wheel_y, 8, 8, 14)

        self.draw_arm()
        self.draw_head()
        self.draw_hand()

        if(debug):
            pyxel.text(4, 4, f"X: {self.x} Y: {self.y}", 0)
            pyxel.line(self.x, 0, self.x, 120, 7)
    
    def draw_mount(self):
        pyxel.blt(self.x - 8, 24, 0, 48, 0, 16, 8, 14)

    def draw_arm(self):
        pyxel.blt(self.x-8, 32,0,48,8, 16, 8, 14)

    def draw_head(self):
        pyxel.blt(self.x-8, 40,0,32,0, 16, 8, 14)

    def draw_hand(self):
        pyxel.blt(self.x-8, 48,0,32,24, 16, 8, 14)

    def update(self):
        if pyxel.btn(pyxel.KEY_LEFT):
            self.x = max(self.x - 2, 0)
        if pyxel.btn(pyxel.KEY_RIGHT):
            self.x = min(self.x + 2, pyxel.width - 16)

App()
