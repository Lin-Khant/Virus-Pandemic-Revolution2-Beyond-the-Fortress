from turtle import Turtle

class UI():

    def __init__(self, player) -> None:
        self.huge_font = ("Times New Roman", 80, "bold")
        self.medium_font = ("Times New Roman", 30, "bold")
        self.small_font = ("Times New Roman", 20, "bold")
        self.player = player
        self.pens = []  # list of indicators
        self.pen_count = 6
        for i in range(self.pen_count):
            new_pen = Turtle()
            new_pen.hideturtle()
            new_pen.speed(0)
            new_pen.penup()
            new_pen.in_game = False
            self.pens.append(new_pen)
        # Special setups for each indicator
        self.lives_indicator = self.pens[0]
        self.lives_indicator.goto(-720, 270)
        self.lives_indicator.color("#d70000")
        self.health_indicator = self.pens[1]
        self.health_indicator.goto(-650, 350)
        self.health_indicator.color("#d70000")
        self.shield_indicator = self.pens[2]
        self.shield_indicator.goto(-650, 310)
        self.shield_indicator.color("#0089d7")
        self.score_indicator = self.pens[3]
        self.score_indicator.goto(-650, 270)
        self.zone_indicator = self.pens[4]
        self.zone_indicator.sety(365)
        self.notification = self.pens[5]

    def updateLives(self):
        self.lives_indicator.clear()
        self.lives_indicator.write(self.player.lives, False, "left", self.huge_font)  

    def updateHealth(self):
        self.health_indicator.clear() 
        self.health_indicator.write(f"Health : {self.player.health}", False, "left", self.small_font)

    def updateShields(self, stacks = 0):
        self.shield_indicator.clear()
        self.shield_indicator.write(f"Shields : {stacks}", False, "left", self.small_font)
        
    def updateScore(self):
        self.score_indicator.clear()
        self.score_indicator.write(f"Score : {self.player.score}", False, "left", self.small_font)

    def updateZone(self):
        self.zone_indicator.clear()
        self.zone_indicator.write(f"Zone {self.player.current_zone + 1}/3", False, "center", self.small_font)
    
    # Update all data
    def updateInfo(self):
        for pen in self.pens:
            pen.clear()
        self.updateLives()
        self.updateHealth()
        self.updateShields()
        self.updateScore()
        self.updateZone()