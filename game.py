import os
import time
from board import *
from mando import *
from headerfile import *


obj_board=Screen(HEIGHT,MAXWIDTH)

obj_mando=Mando(0,0)  #run,fly




counter=3
timetrack=time.time()

obj_mando.place_mando(counter,HEIGHT-3,obj_board.grid)
while True:
    if time.time() - timetrack >= 0.15:
        os.system('clear')
        timetrack=time.time()
        obj_mando.erase_mando(obj_board.grid)
        obj_mando.generate_shape()
        obj_mando.place_mando(counter,HEIGHT-3,obj_board.grid)
        obj_board.show_all()

        if counter<MAXWIDTH-WIDTH:
            counter+=1



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
