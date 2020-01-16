import os
import time
from board import *
from mando import *
from scenery import *
from headerfile import *
from alarmexception import *
import signal
from getch import _getChUnix as getChar


def alarmhandler(signum, frame):
    ''' input method '''
    raise AlarmException


def user_input(timeout=0.15):
    ''' input method '''
    signal.signal(signal.SIGALRM, alarmhandler)
    signal.setitimer(signal.ITIMER_REAL, timeout)

    try:
        text = getChar()()
        signal.alarm(0)
        return text
    except AlarmException:
        pass
    signal.signal(signal.SIGALRM, signal.SIG_IGN)
    return '.'


obj_board = Screen(HEIGHT, MAXWIDTH)
obj_mando = Mando(0, 0)  # run,fly

obj_scenery = Scenery()
obj_scenery.create_ground(obj_board.grid)
obj_scenery.create_sky(obj_board.grid)

counter = 3
timetrack = time.time()
starttime = time.time()

# obj_mando.place_mando(counter,HEIGHT-3,obj_board.grid)
# obj_board.show_all()
refreshcount = 0
while True:
    if time.time() - timetrack >= 0.15:
        timetrack = time.time()
        obj_mando.erase_mando(obj_board.grid)

        letter = user_input()
        if letter == 'q':
            quit()
        elif letter == 'd':
            # set 3rd arg as -100 if want to keep in air on d
            obj_mando.set_values(5, 1, 0, counter)
            refreshcount = 0
        elif letter == 'a':
            # set 3rd arg as -100 if want to keep in aiif counter < MAXWIDTH-WIDTH on w
            obj_mando.set_values(-3, -1, 0, counter)
            refreshcount = 0
        elif letter == 'w':
            # unsure if second arg should be 0 or -100
            if counter < MAXWIDTH-WIDTH:
                obj_mando.set_values(1, 0, 1, counter)
            else:
                obj_mando.set_values(0, 0, 1, counter)
            refreshcount = 0
        elif refreshcount == 2:
            if counter < MAXWIDTH-WIDTH:
                obj_mando.set_values(1, 0, 0, counter)
            else:
                obj_mando.set_values(0, 0, 0, counter)
            refreshcount = 0
        else:
            # obj_mando.set_values(1,0,0)
            if counter < MAXWIDTH-WIDTH:
                obj_mando.set_values(1, -100, -100, counter)
            else:
                obj_mando.set_values(0, -100, -100, counter)
            refreshcount += 1

        obj_mando.generate_shape()
        obj_mando.place_mando(obj_board.grid)

        timeleft = 150 - (round(time.time()) - round(starttime))
        if timeleft <= 0:
            print('Time Up!!')
            break

        os.system('clear')
        print("Time:", 150 -
              (round(time.time()) - round(starttime)))
        print(Fore.YELLOW + "$$:" + Fore.RESET, obj_mando.coins)
        obj_board.show_board(counter)
        # obj_board.show_all()

        if counter < MAXWIDTH-WIDTH:
            counter += 1


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
