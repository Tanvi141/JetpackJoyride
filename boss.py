from obstacles import *
from headerfile import *
import numpy as np
import random

class Boss(Obstacles):

    def __init__(self,lives):
        super().__init__(lives)
        a = np.zeros((8, 50), dtype='<U20')
        a[:] = ' '
        y = 0
        with open("dragon.txt") as obj:
            for line in obj:
                x = 0
                for char in line:
                    if char == '\n':
                        break
                    else:
                        a[y][x] = char+Fore.RESET
                    x += 1
                y += 1
        self.__body = a
        self._xrange = 50
        self._yrange = 8

    def position_boss(self, obj_mando, grid):

        grid[self._y:self._y+self._yrange, self._x:self._x+self._xrange][:] = ' '

        y = obj_mando.get_y()
        self._y = y-4

        if y+self._yrange > HEIGHT-GROUND:
            self._y = HEIGHT-GROUND-self._yrange
        elif self._y < SKY:
            self._y = SKY

        self._x = MAXWIDTH-self._xrange-2

    def place(self, grid):
        grid[self._y:self._y+self._yrange,
             self._x:self._x+self._xrange] = self.__body

        for i in range(self._y,self._y+self._yrange):
            for j in range(self._x,self._x+self._xrange):
                if(random.randint(0,1)==1): 
                    grid[i][j]=Fore.RED+grid[i][j]
                else:
                    grid[i][j]=Fore.YELLOW+grid[i][j]

    def fire(self,iceballs,obj_mando):
        iceballs.append(IceBalls(self._x,obj_mando.get_y()))


class IceBalls():

    def __init__(self, x, y):

        self.__x = x
        self.__y = y
        self.__killed = 0
        self.__shape = np.zeros((3, 3), dtype='<U20')
        self.__shape[0] = [WHITE+'*'+RESET, ICE+'x'+RESET, WHITE+'*'+RESET]
        self.__shape[1] = [ICE+'x'+RESET, ICE+'x'+RESET, ICE+'x'+RESET]
        self.__shape[2] = [WHITE+'*'+RESET, ICE+'x'+RESET, WHITE+'*'+RESET]


    def place_bullet(self, grid):
        '''Places bullet on the board then moves it forward
        '''
        self.__x -= 2

        if self.__x < MAXWIDTH-WIDTH-3:
            self.__killed = 1

        if self.__killed == 0:
            y = self.__y
            x = self.__x
            grid[y-1:y+2, x-1:x+2] = self.__shape

    def move_bullet(self, grid):
        y = self.__y
        x = self.__x
        grid[y-1:y+2, x-1:x+2][:] = ' '

    def check_collision_mando(self, obj_mando):
        if obj_mando.get_shield()==1 or self.__killed==1:
            return
        x = obj_mando.get_x()
        y = obj_mando.get_y()

        if(x+1 >= self.__x and x-1 <= self.__x+2 and y+1 >= self.__y-1 and y-1 <= self.__y+1):
            obj_mando.kill_mando()
            os.system("aplay funstuff/mandodie.wav -q &")
            obj_mando.change_score(-50)

        
