from turtle import Screen, Turtle
import padel

screen = Screen()
screen.bgcolor("blue")
screen.setup(width=800, height=600)
screen.title("Ping Pong")
screen.tracer(0)

PADEL_POS_R = (350,0)
PADEL_POS_L = (-350,0)

padel_r = padel.Padel(PADEL_POS_R)
padel_l = padel.Padel(PADEL_POS_L)

screen.listen()

screen.onkey(padel_r.go_up, "Up")
screen.onkey(padel_r.go_dn, "Down")
screen.onkey(padel_l.go_up, 'w')
screen.onkey(padel_l.go_dn, 's')



game_is_on = True
while game_is_on:
    screen.update()



screen.exitonclick()