# The speed of the virus might change on different devices.
# To change the virus move_speed and virus impact(player speed reduction upon infection),
# pls go to --> game_manager.py > GameManager() > spawnViruses()

from turtle import Turtle

class Virus(Turtle):

    def __init__(self, shape, death_shape, speed, dmg, imp, resistance, bonus) -> None:
        super().__init__()
        self.speed(0)
        self.hideturtle()
        self.shape(shape)
        self.penup()
        self.death_vfx = Turtle(death_shape)
        self.death_vfx.speed(0)
        self.death_vfx.hideturtle()
        self.death_vfx.penup()
        self.in_game = False
        self.move_speed = speed
        self.damage = dmg
        self.impact = imp
        self.resistance = resistance
        self.original_resistance = resistance
        self.score_bonus = bonus

    def move(self):
        if self.in_game != False:
            x = self.xcor()
            x -= self.move_speed/100
            self.setx(x)

    def clearVFX(self):
        self.death_vfx.hideturtle()

    def destroy(self):
        self.death_vfx.goto(self.position())
        self.death_vfx.showturtle()

    def dealDMG(self, receiver, x, y):
        self.goto(x, y)
        receiver.infected_times += 1
        new_score = receiver.score - (10 + self.score_bonus)
        new_speed = receiver.move_speed - self.impact
        receiver.health -= self.damage
        if new_score < 0:
            receiver.score = 0
        else:
            receiver.score = new_score

        if new_speed < 5:
            receiver.move_speed = 5
        else:
            receiver.move_speed = new_speed

        if receiver.health <= 0:
            receiver.health = 0
            receiver.lives -= 1
            if receiver.lives < 1:
                receiver.death()
            else:
                receiver.revive()

        receiver.weapon.damage = receiver.health/2
        if receiver.weapon.damage > 100:
            receiver.weapon.damage = 100