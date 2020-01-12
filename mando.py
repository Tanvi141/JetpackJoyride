import numpy as np
from headerfile import *


class Mando:
    '''Define the mando
    '''

    def __init__(self, dirn, fly):
        self.__x = 3  # x coordinate of the torso
        self.__y = 3  # y coordinate of the torso
        self.__dirn = dirn  # -1 means left, 0 means stop, 1 means right
        self.__fly = fly    # 1 means flying, 0 means not

        self.__body = np.zeros((3, 3), dtype='<U20')
        self.__body[:] = ' '
        # creating an empty array to make erasing easier
        self.__empty = np.zeros((3, 3), dtype='<U20')
        self.__empty[:] = ' '

    def generate_shape(self):
        '''Gives Mando's body appropriate shape according to dirn and type of movement
        '''
        if self.__fly == 1:
            self.__body[0] = ['\\', CYAN+'0'+RESET, '/']
            self.__body[1] = [' ', '|', ' ']

        else:
            self.__body[0] = [' ', CYAN+'0'+RESET, ' ']
            self.__body[1] = ['/', '|', '\\']

        if self.__dirn == 0:
            self.__body[2] = ['/', ' ', '\\']

        elif self.__dirn == -1:
            self.__body[2] = ['<', ' ', '\\']

        else:
            self.__body[2] = ['/', ' ', '>']

    def place_mando(self, x, y, grid):
        '''Places the mando at appropriate position with torso at x,y
        '''
        grid[y-1:y+2, x-1:x+2] = self.__body
        self.__x=x
        self.__y=y

    def erase_mando(self, grid):
        '''Erases mando off the board
        '''
        x = self.__x
        y = self.__y
        grid[y-1:y+2, x-1:x+2] = self.__empty
