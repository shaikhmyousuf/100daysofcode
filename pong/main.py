from turtle import Screen, Turtle
screen = Screen()
screen.bgcolor("blue")
screen.setup(width=800, height=600)
screen.title("Ping Pong")
screen.tracer(0)

padel_right = Turtle()
padel_right.shape("square")
padel_right.color("white")
padel_right.shapesize(stretch_wid=5, stretch_len=1)
padel_right.penup()
padel_right.goto(350, 0)
 
def go_up():
    snew_y = padel_right.ycor() + 20
    padel_right.sety(new_y)

def go_down():
    new_y = padel_right.ycor() - 20
    padel_right.sety(new_y)

screen.listen()
screen.onkey(go_up, "Up")
screen.onkey(go_down, "Down")

game_is_on = True
while game_is_on:
    screen.update()



screen.exitonclick()