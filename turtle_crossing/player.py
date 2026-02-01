from turtle import Turtle

STARTING_POSITION = (0, -280)
MOVE_DISTANCE = 10
FINISH_LINE_Y = 280


class Player(Turtle):
    def __init__(self):
        super().__init__()
        self.shape("turtle")
        self.color("blue")
        self.penup()
        self.setheading(90)
        self.goto_start()
    
    def go_up(self):
        new_y = self.ycor()+10
        self.sety(new_y)

    def go_dn(self):
        new_y = self.ycor()-10
        self.sety(new_y)

    def is_at_finishline(self):
        if self.ycor() > FINISH_LINE_Y:
            return True
        else:
            return False

    def goto_start(self):
        self.goto(STARTING_POSITION)
        