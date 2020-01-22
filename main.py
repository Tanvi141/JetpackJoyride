import os
import time
import signal
import random

from headerfile import *
from alarmexception import *
from getch import *
from board import *
from mando import *
from obstacles import *
from scenery import *
from powerups import *
from bullets import *
from boss import *

def showmessage(msg,obj_mando):
    # os.system("clear")
    print("\n\n")
    if msg == "Time Up!!":
        print("\t\t\t _______  ___   __   __  _______    __   __  _______\n" +
              "\t\t\t|       ||   | |  |_|  ||       |  |  | |  ||       |\n" +
              "\t\t\t|_     _||   | |       ||    ___|  |  | |  ||    _  |\n" +
              "\t\t\t  |   |  |   | |       ||   |___   |  |_|  ||   |_| |\n" +
              "\t\t\t  |   |  |   | |       ||    ___|  |       ||    ___|\n" +
              "\t\t\t  |   |  |   | | ||_|| ||   |___   |       ||   |\n" +
              "\t\t\t  |___|  |___| |_|   |_||_______|  |_______||___|\n")
    
    elif msg =="You won!!":
        print( "\t\t\t __   __  ___   _______  _______  _______  ______    __   __\n" +   
               "\t\t\t|  | |  ||   | |       ||       ||       ||    _ |  |  | |  |\n" +  
               "\t\t\t|  |_|  ||   | |      _||_     _||   _   ||   | ||  |  |_|  |\n" +  
               "\t\t\t|       ||   | |     |    |   |  |  | |  ||   |_||_ |       |\n" +  
               "\t\t\t|       ||   | |     |    |   |  |  |_|  ||    __  ||_     _|\n" +  
               "\t\t\t |     | |   | |     |_   |   |  |       ||   |  | |  |   |\n" +    
               "\t\t\t  |___|  |___| |_______|  |___|  |_______||___|  |_|  |___|\n" )
    
    elif msg=="Lives over!!":
        print("\t\t\t _______  _______  __   __  _______    _______  __   __  _______  ______\n" +  
              "\t\t\t|       ||   _   ||  |_|  ||       |  |       ||  | |  ||       ||    _ |\n"  +
              "\t\t\t|    ___||  |_|  ||       ||    ___|  |   _   ||  |_|  ||    ___||   | ||\n"  +
              "\t\t\t|   | __ |       ||       ||   |___   |  | |  ||       ||   |___ |   |_||_\n" +
              "\t\t\t|   ||  ||       ||       ||    ___|  |  |_|  ||       ||    ___||    __  |\n"+
              "\t\t\t|   |_| ||   _   || ||_|| ||   |___   |       | |     | |   |___ |   |  | |\n"+
              "\t\t\t|_______||__| |__||_|   |_||_______|  |_______|  |___|  |_______||___|  |_|\n")
    

    elif msg=="Quit!!":
        print("\t\t\t __   __  _______  __   __    _______  __   __  ___   _______ \n" +
              "\t\t\t|  | |  ||       ||  | |  |  |       ||  | |  ||   | |       |\n" +
              "\t\t\t|  |_|  ||   _   ||  | |  |  |   _   ||  | |  ||   | |_     _|\n" +
              "\t\t\t|       ||  | |  ||  |_|  |  |  | |  ||  |_|  ||   |   |   |  \n" +
              "\t\t\t|_     _||  |_|  ||       |  |  |_|  ||       ||   |   |   |  \n" +
              "\t\t\t  |   |  |       ||       |  |      | |       ||   |   |   |  \n" +
              "\t\t\t  |___|  |_______||_______|  |____||_||_______||___|   |___|  \n" )

    print("\n\n")

    if (msg!="Quit!!"):
        print("\t\t\t\t Score: ", obj_mando.get_score())

    print("\n\n")



os.system("aplay -q funstuff/Jetpack-Joyride-Theme-Song.wav &")

obj_board = Screen(HEIGHT, MAXWIDTH)
obj_mando = Mando(0, 0)  # run,fly
obj_boss = Boss(30)

obj_scenery = Scenery()
obj_scenery.create_ground(obj_board.give_grid())
obj_scenery.create_sky(obj_board.give_grid())

counter = 3
timetrack = time.time()
starttime = time.time()
refreshcount = 0

obst = generate_obstacles(obj_board.give_grid(), 3, 2)
coins = generate_coins(obj_board.give_grid(), 100)

counterinc = 1
bullets = []
iceballs = []
firetrack = 0

obj_shield = Shield(60, 10)
obj_speedboost = SpeedBoost(2, 15)

os.system("clear")

print(Back.MAGENTA)
for i in range(4):
    for j in range(WIDTH):
        print(' ', end='')
    print()
print(Back.RESET)

while True:

    if time.time() - timetrack >= 0.15:
        timetrack = time.time()

        counterinc = obj_speedboost.update(obj_mando)
        obj_shield.update(obj_mando)

        obj_mando.erase_mando(obj_board.give_grid(), counterinc)
        for ob in obst:
            ob.place(obj_board.give_grid())

        obj_mando.update_old()

        letter = user_input()
        if letter == "q":
            showmessage("Quit!!",obj_mando)
            break
        elif letter == "d":
            # set 3rd arg as -100 if want to keep in air on d
            obj_mando.set_values(counterinc+4, 1, 0, counter)
            refreshcount = 0
        elif letter == "a":
            # set 3rd arg as -100 if want to keep in aiif counter < MAXWIDTH-WIDTH on w
            obj_mando.set_values(counterinc-5, -1, 0, counter)
            refreshcount = 0
        elif letter == "w":
            # unsure if second arg should be 0 or -100
            if counter < MAXWIDTH-WIDTH:
                obj_mando.set_values(
                    counterinc, 0, 1, counter)
            else:
                obj_mando.set_values(
                    0, 0, 1, counter)
            refreshcount = 0
        elif refreshcount == 2:
            if counter < MAXWIDTH-WIDTH:
                obj_mando.set_values(
                    counterinc, 0, 0, counter)
            else:
                obj_mando.set_values(
                    0, 0, 0, counter)
            refreshcount = 0
        else:
            if counter < MAXWIDTH-WIDTH:
                obj_mando.set_values(
                    counterinc, -100, -100, counter)
            else:
                obj_mando.set_values(
                    0, -100, -100, counter)
            refreshcount += 1

        if letter == "l":
            obj_speedboost.activate()
        elif letter == " ":
            obj_shield.activate()
        elif letter == "k":
            bullets.append(Bullets(obj_mando))

        obj_mando.generate_shape()

        if counter < MAXWIDTH-WIDTH:
            counter += counterinc

        for bulls in bullets:
            for beams in obst:
                beams.check_collision_bullets(
                    bulls, obj_board.give_grid(), counterinc, obj_mando)

        for bulls in bullets:
            bulls.move_bullet(obj_board.give_grid(), counterinc)

        for bulls in bullets:
            bulls.place_bullet(obj_board.give_grid(), counter)

        obj_mando.set_airtime()

        for i in range(int(obj_mando.get_airtime()*obj_mando.get_airtime()/2)+1):
            if i != 0:
                obj_mando.erase_mando(obj_board.give_grid(), counterinc)
            obj_mando.change_y_mando()

            for ob in obst:
                ob.check_collision_mando(obj_mando, counter)
            obj_mando.place_mando(obj_board.give_grid(), counterinc)

        if counter >= MAXWIDTH-WIDTH:
            firetrack += 1
            obst = []
            for ice in iceballs:
                ice.check_collision_mando(obj_mando)

            obj_boss.position_boss(obj_mando, obj_board.give_grid())
            obj_boss.place(obj_board.give_grid())
            if(firetrack % 4 == 0):
                obj_boss.fire(iceballs, obj_mando)

            for ice in iceballs:
                ice.move_bullet(obj_board.give_grid())

            for ice in iceballs:
                ice.place_bullet(obj_board.give_grid())

            for bulls in bullets:
                obj_boss.check_collision_bullets(
                    bulls, obj_board.give_grid(), counterinc, obj_mando)

        obj_mando.place_mando(obj_board.give_grid(), counterinc)

        for c in coins:
            obj_mando.check_coin(c, obj_board.give_grid())

        obj_mando.place_mando(obj_board.give_grid(), counterinc)

        # os.system("clear")
        print("\033[%d;%dH" % (0, 0))
        print(Fore.WHITE)
        print(Back.MAGENTA + "Time:",  100 -
              (round(time.time()) - round(starttime)), ' ', end="\t\t\t\t")
        print(Back.MAGENTA+"Lives:", obj_mando.get_lives(), end="\t\t\t\t")
        if counter >= MAXWIDTH-WIDTH-10:
            print(Back.MAGENTA+"the end is near   BOSS LIVES: ",
                  obj_boss.get_lives(), ' ', end="\t\t\t\t")
        print()
        print(Back.MAGENTA+"SpeedUp: " + obj_speedboost.status(), end="\t\t\t")
        print(Back.MAGENTA+"Shield: " + obj_shield.status(), end="\t\t\t\t")
        print()
        print(COIN+":", obj_mando.get_coins(), end="\t\t\t\t\t")
        print(Back.MAGENTA+"Score:", obj_mando.get_score(), end="\t\t\t\t")
        print(RESET)
        obj_board.show_board(counter)

        timeleft = 100 - (round(time.time()) - round(starttime))
        if timeleft <= 0:
            showmessage("Time Up!!",obj_mando)
            break

        if obj_boss.get_lives() == 0:
            showmessage("You won!!",obj_mando)
            obj_mando.change_score(100)
            break

        if obj_mando.get_lives() == 0:
            showmessage("Lives over!!",obj_mando)
            break

os.system("killall aplay -q")



#   0 |
#     |
#     |
#     |
#     |y
#     |
#     |     grid[y][x]
#     |
#     |
#     |
#   H |
#   __|_________________x______________________
#     |0                                       MAXWIDTH


# bulls delete unsued bullets
