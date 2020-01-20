from headerfile import *
import numpy as np
from mando import *
import random


class Obstacles:

    def __init__(self, lives):
        self._killed = 0
        self._lives = 1  # boss should have more lives
        self._x = 0  # declaring variable with some dummy value
        self._y = 0  # declaring variable with some dummy value
        self._xrange = 0  # declaring variable with some dummy value
        self._yrange = 0  # declaring variable with some dummy value
        self.__killflag = 0  # this is used to make sure that once mando comes into contact with laser once he won't lose more than one life at a time

    def overlap(self, grid):
        '''returns 0 if can correctly place, else returns 1
        '''
        m = grid[self._y-1:self._y+self._yrange+1, self._x-1:self._x +
                 self._xrange+1]  # padding of spaces set around this
        if np.count_nonzero(m == ' ') != (self._yrange+2)*(self._xrange+2):
            return 1
        else:
            return 0

    def place(self, grid):
        pass

    def check_collision_mando(self, obj_mando):
        '''returns 1 if mando has collided with this object
        '''
        if obj_mando.shield == 1 or self._killed == 1:
            return obj_mando.lives

        x = obj_mando.get_x()
        y = obj_mando.get_y()

        # sdf,df,legs,head
        if x+1 >= self._x and x-1 < self._x + self._xrange and y+1 >= self._y and y-1 < self._y+self._yrange:
            # then mando is being hit by laser
            if self.__killflag == 0:
                # so he has just come into contact with the laser
                obj_mando.lives -= 1
            else:
                # he keeps moving through the same
                pass
            self.__killflag = 1

        else:
            # he is not in contact with the laser
            self.__killflag = 0

        return obj_mando.lives

    def check_collision_bullets(self, obj_bullet,grid,counterinc):
        if obj_bullet.killed() or self._killed == 1:
            return

        x = obj_bullet.get_x()
        y = obj_bullet.get_y()

        if x+4+counterinc >= self._x and x-1 < self._x + self._xrange and y >= self._y and y < self._y+self._yrange:
            obj_bullet.kill(grid)
            self._killed = 1


class HorizontalBeam(Obstacles):

    def __init__(self, x, y):
        super().__init__(1)
        self._x = x
        self._y = y
        self._xrange = 24
        self._yrange = 2

    def place(self, grid):
        if(self._killed) == 1:
            grid[self._y:self._y+self._yrange, self._x:self._x +
                 self._xrange] = np.tile([' '], (self._yrange, self._xrange))
        else:
            grid[self._y:self._y+self._yrange, self._x:self._x +
                 self._xrange] = np.tile([STAR], (self._yrange, self._xrange))


class VerticalBeam(Obstacles):

    def __init__(self, x, y):
        super().__init__(1)
        self._x = x
        self._y = y
        self._xrange = 2
        self._yrange = 12

    def place(self, grid):
        if(self._killed) == 1:
            grid[self._y:self._y+self._yrange, self._x:self._x +
                 self._xrange] = np.tile([' ', ' '], (self._yrange, (int)(self._xrange/2)))

        else:
            grid[self._y:self._y+self._yrange, self._x:self._x +
                 self._xrange] = np.tile([STAR, STAR], (self._yrange, (int)(self._xrange/2)))


class DiagonalBeam(Obstacles):

    def __init__(self, x, y):
        super().__init__(1)
        self._x = x
        self._y = y
        self._yrange = 8
        self._xrange = self._yrange*2

    def place(self, grid):
        if(self._killed) == 1:
            for i in range(self._yrange):
                grid[self._y+i][self._x+2*i] = ' '
                grid[self._y+i][self._x+2*i+1] = ' '
        else:
            for i in range(self._yrange):
                grid[self._y+i][self._x+2*i] = STAR
                grid[self._y+i][self._x+2*i+1] = STAR

class CoinBeam(Obstacles):
    
    def __init__(self,x,y,xrange,yrange):
        super().__init__(1)
        self._x=x
        self._y=y
        self._xrange=xrange
        self._yrange=yrange
        
    def place(self, grid):
        grid[self._y:self._y+self._yrange, self._x:self._x +
                 self._xrange] = np.tile([COIN], (self._yrange, self._xrange))

def generate_lasers(grid):

    obst = []

    for i in range(5):
        x = random.randint(PLACEWIDTH+5, MAXWIDTH-WIDTH-10)
        y = random.randint(SKY+1, HEIGHT-GROUND-1)
        obj = DiagonalBeam(x, y)

        while(obj.overlap(grid)):
            x = random.randint(PLACEWIDTH+5, MAXWIDTH-WIDTH-10)
            y = random.randint(SKY+1, HEIGHT-GROUND-1)
            # print(x,y)
            obj = DiagonalBeam(x, y)
        obj.place(grid)
        obst.append(obj)

        x = random.randint(PLACEWIDTH+5, MAXWIDTH-WIDTH-10)
        y = random.randint(SKY+1, HEIGHT-GROUND-1)
        obj = HorizontalBeam(x, y)

        while(obj.overlap(grid)):
            x = random.randint(PLACEWIDTH+5, MAXWIDTH-WIDTH-10)
            y = random.randint(SKY+1, HEIGHT-GROUND-1)
            # print(x,y)
            obj = HorizontalBeam(x, y)
        obj.place(grid)
        obst.append(obj)

        x = random.randint(PLACEWIDTH+5, MAXWIDTH-WIDTH-10)
        y = random.randint(SKY+1, HEIGHT-GROUND-1)
        obj = VerticalBeam(x, y)

        while(obj.overlap(grid)):
            x = random.randint(PLACEWIDTH+5, MAXWIDTH-WIDTH-10)
            y = random.randint(SKY+1, HEIGHT-GROUND-1)
            # print(x,y)
            obj = VerticalBeam(x, y)
        obj.place(grid)
        obst.append(obj)

    obst.sort(key=lambda obj: obj._x, reverse=False)
    return obst

def generate_coins(grid):

    for i in range(20):
        x = random.randint(PLACEWIDTH+5, MAXWIDTH-WIDTH-10)
        y = random.randint(SKY+1, HEIGHT-GROUND-4)
        obj = CoinBeam(x,y,16,3)

        # while(obj.overlap(grid)):
        #     x = random.randint(PLACEWIDTH+5, MAXWIDTH-WIDTH-10)
        #     y = random.randint(SKY+1, HEIGHT-GROUND-1)
        obj.place(grid)