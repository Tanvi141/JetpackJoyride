import numpy as np
from headerfile import *
import time
 

class Bullets():
    #(x-1,y), (x,y)
    def __init__(self,obj_mando):
        
        self.__x=obj_mando.get_x()+2
        self.__y=obj_mando.get_y()
        self.__killed=0
        self.__old1=' '
        self.__old2=' '

    def killed(self):
        return self.__killed

    def kill(self,grid):
        self.__killed=1
        grid[self.__y][self.__x]=self.__old1
        grid[self.__y][self.__x-1]=self.__old2

    def place_bullet(self,grid,counter):
        '''Places bullet on the board then moves it forward
        '''
        if self.__x<counter or self.__x>counter+WIDTH or self.__x+5>MAXWIDTH:
            self.__killed=1

        if self.__killed==0:
            self.__old1=grid[self.__y][self.__x]
            self.__old2=grid[self.__y][self.__x-1]
            grid[self.__y][self.__x]=">"
            grid[self.__y][self.__x-1]="="

    def move_bullet(self,grid,counterinc):
        if self.__killed==0:
            grid[self.__y][self.__x]=self.__old1
            grid[self.__y][self.__x-1]=self.__old2
            self.__x+=4+counterinc
    
    def get_x(self):
        return self.__x

    def get_y(self):
        return self.__y

    #check collision, move, place
