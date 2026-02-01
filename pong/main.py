from turtle import Screen, Turtle
import padel
import ball
import time
import scoreboard

screen = Screen()
screen.bgcolor("blue")
screen.setup(width=800, height=600)
screen.title("Ping Pong")
screen.tracer(0)

PADEL_POS_R = (350,0)
PADEL_POS_L = (-350,0)

padel_r = padel.Padel(PADEL_POS_R)
padel_l = padel.Padel(PADEL_POS_L)
ball    = ball.Ball()
scoreboard = scoreboard.Scoreboard()

screen.listen()

screen.onkey(padel_r.go_up, "Up")
screen.onkey(padel_r.go_dn, "Down")
screen.onkey(padel_l.go_up, 'w')
screen.onkey(padel_l.go_dn, 's')



game_is_on = True
while game_is_on:
    time.sleep(ball.move_speed)
    screen.update()
    ball.move()

    if ball.ycor() > 280 or ball.ycor() < -280:
        ball.bounce_y()
    
    if ball.distance(padel_r) < 55 and ball.xcor() > 320\
        or ball.distance(padel_l) < 55 and ball.xcor() < -320:
        ball.bounce_x()

    if ball.xcor() > 400:
        ball.reset()
        scoreboard.point_l()
        scoreboard.update_scoreboard()


    if ball.xcor() < -400:
        ball.reset()
        scoreboard.point_r()
        scoreboard.update_scoreboard()

screen.exitonclick()