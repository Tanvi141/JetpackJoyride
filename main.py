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


obj_board = Screen(HEIGHT, MAXWIDTH)
obj_mando = Mando(0, 0)  # run,fly
obj_boss=Boss()

obj_scenery = Scenery()
obj_scenery.create_ground(obj_board.grid)
obj_scenery.create_sky(obj_board.grid)

counter = 3
timetrack = time.time()
starttime = time.time()
refreshcount = 0

generate_coins(obj_board.grid)
obst = generate_lasers(obj_board.grid)
counterinc=1
bullets=[]
iceballs=[]
firetrack=0

obj_shield=Shield(10,10)
obj_speedboost=SpeedBoost(2,15)

while True:

    if time.time() - timetrack >= 0.15:
        timetrack = time.time()

        counterinc=obj_speedboost.update(obj_mando)
        obj_shield.update(obj_mando)

        obj_mando.erase_mando(obj_board.grid,counterinc)
        for ob in obst:
            ob.place(obj_board.grid)

        letter = user_input()
        if letter == 'q':
            quit()
        elif letter == 'd':
            # set 3rd arg as -100 if want to keep in air on d
            obj_mando.set_values(counterinc+3, 1, 0, counter, obj_board.grid)
            refreshcount = 0
        elif letter == 'a':
            # set 3rd arg as -100 if want to keep in aiif counter < MAXWIDTH-WIDTH on w
            obj_mando.set_values(counterinc-3, -1, 0, counter, obj_board.grid)
            refreshcount = 0
        elif letter == 'w':
            # unsure if second arg should be 0 or -100
            if counter < MAXWIDTH-WIDTH:
                obj_mando.set_values(   
                    counterinc, 0, 1, counter, obj_board.grid)
            else:
                obj_mando.set_values(
                    0, 0, 1, counter, obj_board.grid)
            refreshcount = 0
        elif refreshcount == 2:
            if counter < MAXWIDTH-WIDTH:
                obj_mando.set_values(
                    counterinc, 0, 0, counter, obj_board.grid)
            else:
                obj_mando.set_values(
                    0, 0, 0, counter, obj_board.grid)
            refreshcount = 0
        else:
            if counter < MAXWIDTH-WIDTH:
                obj_mando.set_values(
                    counterinc, -100, -100, counter, obj_board.grid)
            else:
                obj_mando.set_values(
                    0, -100, -100, counter, obj_board.grid)
            refreshcount += 1

        if letter=='l':
            obj_speedboost.activate()
        elif letter==' ':
            obj_shield.activate()
        elif letter=='k':
            bullets.append(Bullets(obj_mando))

        obj_mando.generate_shape()
        
        if counter < MAXWIDTH-WIDTH:
            counter += counterinc

        for bulls in bullets:
            for beams in obst:
                beams.check_collision_bullets(bulls,obj_board.grid,counterinc)

        for bulls in bullets:
            bulls.move_bullet(obj_board.grid,counterinc)
            bulls.place_bullet(obj_board.grid,counter)

        obj_mando.set_airtime()
        for i in range(int(obj_mando.airtime*obj_mando.airtime/2)+1):
            if i!=0:
                obj_mando.erase_mando(obj_board.grid,counterinc)
            obj_mando.change_y_mando()

            for ob in obst:
                ob.check_collision_mando(obj_mando) 
            obj_mando.place_mando(obj_board.grid,counterinc)


        if counter >= MAXWIDTH-WIDTH:
            firetrack+=1
            obst=[]
            for ice in iceballs:
                ice.check_collision_mando(obj_mando)

            obj_boss.position_boss(obj_mando,obj_board.grid)
            obj_boss.place(obj_board.grid)
            if(firetrack%4==0):
                obj_boss.fire(iceballs,obj_mando)

            for ice in iceballs:
                ice.move_bullet(obj_board.grid)
            
            for ice in iceballs:
                ice.place_bullet(obj_board.grid)

            for bulls in bullets:
                obj_boss.check_collision_bullets(bulls,obj_board.grid,counterinc)
       
        obj_mando.place_mando(obj_board.grid,counterinc)

        timeleft = 150 - (round(time.time()) - round(starttime))
        if timeleft <= 0:
            print('Time Up!!')
            break

        if obj_boss.get_lives()==0:
            print('You won!!')
            break

        if obj_mando.lives==0:
            print('Lives over!!')
            break

        os.system('clear')
        print("Time:", 150 -
              (round(time.time()) - round(starttime)), end='\t\t\t')
        print("Lives:", obj_mando.lives, end='\t\t\t')
        if counter >= MAXWIDTH-WIDTH: print("the end is near BOSS LIVES: ", obj_boss.get_lives())
        print("SpeedUp: " + obj_speedboost.status())
        print("Shield: " + obj_shield.status())
        print(Fore.YELLOW + "$$:" + Fore.RESET, obj_mando.coins)
        obj_board.show_board(counter)


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


# bug: press and hold w key, press d once he falls
# bulls delete unsued bullets