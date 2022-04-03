# Player move_speed and attack_speed might change on different devices.
# To slow down the move_speed, pls decrease -> player.move_rate.
# To speed up the move_speed, pls increase -> player.move_rate.
# Attack speed can be changed freely at -> player.weapon.atk_speed.

from turtle import Turtle

class Player(Turtle):

    def __init__(self, shape, bullet, animator) -> None:
        super().__init__()
        self.speed(0)
        self.hideturtle()
        self.idleshape = shape
        self.shape(self.idleshape)
        self.penup()
        self.goto(-600, 0)
        self.in_game = False
        self.is_moving = False
        self.current_zone = 0
        self.viruses_killed = 0
        self.infected_times = 0
        self.items_collected = 0
        self.score = 0
        self.lives = 3
        self.health = 100
        self.move_speed = 30 # <-- don't change this.
        self.move_rate = 1  # <-- change here.
        self.weapon = Turtle(bullet)
        self.weapon.speed(0)
        self.weapon.hideturtle()
        self.weapon.penup()
        self.weapon.in_game = False
        self.weapon.is_ready = True
        self.weapon.atk_speed = 50  # <-- change atk speed here.
        self.weapon.atk_range = 1000
        self.weapon.damage = 50
        self.animator = animator
    
    # start walk animation
    def startAnimation(self):
        if self.is_moving != True:
            self.is_moving = True
        self.hideturtle()
        self.animator.showturtle()

    # go back to idle state
    def stopAnimation(self):
        self.is_moving = False
        self.shape(self.idleshape)
        self.animator.hideturtle()
        self.showturtle()

    # reload the weapon, move the bullet to the player's current position
    def reload(self):
        self.weapon.hideturtle()
        x = self.xcor() + 100
        y = self.ycor() + 40
        self.weapon.goto(x, y)
        self.weapon.in_game = False
        self.weapon.is_ready = True

    def dealDMG(self, target, x, y):
        self.reload()
        target.resistance -= self.weapon.damage
        if target.resistance <= 0:
            target.destroy()
            target.goto(x, y)
            target.resistance = target.original_resistance
            self.score += 10 + target.score_bonus
            self.viruses_killed += 1
        self.animator.screen.ontimer(target.clearVFX, 1000)

    # Secret : the bullet has been moving all time
    def moveBullet(self):
        x = self.weapon.xcor()
        x += self.weapon.atk_speed
        self.weapon.setx(x)

    def fire(self):
        if self.weapon.is_ready and self.weapon.in_game != True:
            self.reload()
            self.weapon.showturtle()
            self.weapon.in_game = True
            self.weapon.is_ready = False
            self.stopAnimation()
            self.shape(self.animator.frames[2])
            self.animator.screen.ontimer(self.stopAnimation, 300)
                    
    def move(self, x_dir, y_dir, speed):
        if self.in_game:
            x = self.xcor()
            x += speed * self.move_rate * x_dir
            if x < -650  or x > 350 and self.current_zone == 2: # x collision detection
                x = self.xcor()
            y = self.ycor()
            y += speed * self.move_rate * y_dir
            if y > 200 or y < -100: # y collision detection
                y = self.ycor()
            self.goto(x, y)
            self.startAnimation()

    def moveRight(self):
        self.move(1, 0, self.move_speed)

    def moveLeft(self):
        self.move(-1, 0, self.move_speed)

    def moveUp(self):
        self.move(0, 1, self.move_speed)

    def moveDown(self):
        self.move(0, -1, self.move_speed)

    def revive(self):
        self.goto(-600, 0)
        self.health = 100
        self.move_speed = 30
        self.weapon.damage = 50
    
    def death(self):
        self.hideturtle()
        self.in_game = False