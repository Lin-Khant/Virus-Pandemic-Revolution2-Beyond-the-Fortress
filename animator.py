# Special file for the player's animations

from turtle import Turtle

class Animator(Turtle):

    def __init__(self, frames, screen) -> None:
        super().__init__()
        self.speed(0)
        self.hideturtle()
        self.penup()
        self.frame_index = 0
        self.frames = frames
        self.screen = screen

    def updatePos(self, player):
        self.goto(player.position())

    # Secret : player's move animation has been playing all time
    def playerWalk(self):
        self.frame_index += 1
        if self.frame_index >= 2:
            self.frame_index = 0
        self.shape(self.frames[self.frame_index])
        self.screen.ontimer(self.playerWalk, 200)   # Recursion