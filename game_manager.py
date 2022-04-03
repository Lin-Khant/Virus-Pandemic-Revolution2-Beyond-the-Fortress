from turtle import Turtle
from virus import Virus
from items import Food
import random

sprites = []    # To receive the sprites imported from main.py
zones = ["./graphics/zone1.gif", "./graphics/zone2.gif", "./graphics/zone3.gif"]
SPAWNPOINTS = (800, 1200, -200, 250, -200, 350)

class GameManager:

    def __init__(self, screen, ui) -> None:
        self.final_result = None
        self.screen = screen
        self.ui = ui
        self.play_btn = Turtle()    # play button
        self.play_btn.hideturtle()
        self.play_btn.speed(0)
        self.play_btn.shape("./graphics/play_btn.gif")
        self.play_btn.penup()

    def registerShapes(self, shape_list):
        for shape in shape_list:
            self.screen.register_shape(shape)

    def setupSprites(self, sprites_list):
        for sprite in sprites_list:
            sprites.append(sprite)

    def switchBG(self, bg):
        self.screen.bgpic(bg)

    # display the final results
    def writeLines(self, pen, display, data):
        for i in range(len(display)):
            pen.goto(-200, pen.ycor() - 100)
            pen.write(f"{display[i]} : {data[i]}", False, "left", self.ui.medium_font)

    def start(self):
        self.switchBG("./graphics/main_bg.gif")
        self.play_btn.goto(-200, -50)
        self.play_btn.showturtle()

    # called by clicking the play button
    def startGame(self, x, y):
        self.play_btn.hideturtle()
        self.play_btn.clear()
        self.switchBG(zones[0])
        for sprite in sprites:
            sprite.showturtle()
            sprite.in_game = True
        for pen in self.ui.pens:
            pen.in_game = True
        self.ui.updateInfo()

    def switchZone(self, player, items):
        self.switchBG(zones[player.current_zone])
        self.ui.updateZone()
        player.setx(-600)
        for item in items:
            item.goto(random.randint(SPAWNPOINTS[4], SPAWNPOINTS[5]), random.randint(SPAWNPOINTS[2], SPAWNPOINTS[3]))
            item.showturtle()
            item.in_game = True

    # virus move_speed and imp (impact) can be changed here.
    def spawnViruses(self, alpha_count, beta_count, delta_count, omicron_count):
        viruses = []
        for i in range(alpha_count):
            viruses.append(Virus("./graphics/alpha.gif", "./graphics/death.gif", speed= 50, dmg= 20, imp= 10, resistance= 50, bonus= 0))
        for i in range(beta_count):
            viruses.append(Virus("./graphics/beta.gif", "./graphics/death.gif", speed= 60, dmg= 30, imp= 15, resistance= 50, bonus= 10))
        for i in range(delta_count):
            viruses.append(Virus("./graphics/delta.gif", "./graphics/death.gif", speed= 80, dmg= 50, imp= 20, resistance= 100, bonus= 20))
        for i in range(omicron_count):
            viruses.append(Virus("./graphics/omicron.gif", "./graphics/death.gif", speed= 120, dmg= 30, imp= 15, resistance= 150, bonus= 30))

        return viruses

    def generateFoods(self, count):
        foods = []
        for i in range(count):
            foods.append(Food("./graphics/food.gif"))
        return foods

    def victory(self, display, data):
        self.screen.clear()
        self.switchBG("./graphics/victory.gif")
        end_pen = Turtle()
        end_pen.hideturtle()
        end_pen.speed(0)
        end_pen.penup()
        end_pen.sety(200)
        end_pen.color("white")
        self.writeLines(end_pen, display, data)

    def gameOver(self, display, data):
        self.screen.clear()
        self.switchBG("./graphics/game_over.gif")
        end_pen = Turtle()
        end_pen.hideturtle()
        end_pen.speed(0)
        end_pen.penup()
        end_pen.sety(200)
        self.writeLines(end_pen, display, data)
