import time
from turtle import Screen
import game_objects.player as player
import game_objects.car_manager as car_manager 
import game_objects.scoreboard as scoreboard 

screen = Screen()
screen.setup(width=600, height=600)
screen.tracer(0)

turtle_player = player.Player()
car_manager = car_manager.CarManager()
score_board = scoreboard.Scoreboard()


screen.listen()
screen.onkey(turtle_player.go_up, "Up")
screen.onkey(turtle_player.go_dn, "Down")

game_is_on = True
while game_is_on:
    time.sleep(0.1)

    screen.update()
    car_manager.create_car()
    car_manager.move_cars()

    '''Detect collisions'''
    for car in car_manager.all_cars:
        if car.distance(turtle_player) < 20:
            game_is_on = False
            score_board.game_over()

    '''Detect successful crossing'''
    if turtle_player.is_at_finishline():
        turtle_player.goto_start()
        car_manager.level_up()
        score_board.increase_level()


screen.exitonclick()