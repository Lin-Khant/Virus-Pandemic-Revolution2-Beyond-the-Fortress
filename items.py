from turtle import Turtle

class Food(Turtle):

    def __init__(self, shape) -> None:
        super().__init__()
        self.speed(0)
        self.hideturtle()
        self.shape(shape)
        self.penup()
        self.in_game = False
        self.diet = 10
        self.energy = 3

    def heal(self, player, x, y):
        self.goto(x, y)
        player.items_collected += 1
        player.health += self.diet
        if player.health > 300:
            player.health = 300
        player.weapon.damage = player.health/2  # Note : player's dmg = player's health/2
        if player.weapon.damage > 100:
            player.weapon.damage = 100
        player.score += 10
        new_speed = player.move_speed + self.energy
        if new_speed >= 50:
            player.move_speed = 50
        else:
            player.move_speed = new_speed


class Mask(Turtle):

    def __init__(self, shape, shield, x, y) -> None:
        super().__init__()
        self.speed(0)
        self.hideturtle()
        self.shape(shape)
        self.penup()
        self.goto(x, y)
        self.in_game = False
        self.shield = Turtle(shield)
        self.shield.speed(0)
        self.shield.hideturtle()
        self.shield.penup()
        self.shield.stacks = 0

    def followPlayer(self, player):
        self.shield.goto(player.position())

    def openShield(self, player):
        if self.in_game:
            self.hideturtle()
            self.in_game = False
            self.shield.showturtle()
            self.shield.stacks += 1
            player.score += 50
            player.items_collected += 1

    def closeShield(self, virus, x, y):
        virus.goto(x, y)
        self.shield.stacks -= 1
        if self.shield.stacks < 1:
            self.shield.hideturtle()


class Medkit(Turtle):

    def __init__(self, shape, x, y) -> None:
        super().__init__()
        self.speed(0)
        self.hideturtle()
        self.shape(shape)
        self.penup()
        self.goto(x, y)
        self.in_game = False
        self.diet = 50
        self.energy = 15

    def superHeal(self, player):
        if self.in_game:
            self.hideturtle()
            self.in_game = False
            player.items_collected += 1
            player.health += self.diet
            if player.health > 300:
                player.health = 300
            player.weapon.damage = player.health/2  # Note : player's dmg = player's health/2
            if player.weapon.damage > 100:
                player.weapon.damage = 100
            player.score += 50
            new_speed = player.move_speed + self.energy
            if new_speed >= 50:
                player.move_speed = 50
            else:
                player.move_speed = new_speed


class Vaccine(Turtle):

    def __init__(self, shape) -> None:
        super().__init__()
        self.speed(0)
        self.hideturtle()
        self.shape(shape)
        self.penup()
        self.goto(530, -80)
        self.in_game = False