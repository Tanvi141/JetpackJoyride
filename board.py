from headerfile import *
import numpy as np


class Screen:
    '''This class creates the grid for the game, and displays it
    '''

    def __init__(self, rows, columns):
        '''Initializes size of grid
        '''
        self.__rows = rows
        self.__columns = columns
        self.grid = np.zeros((HEIGHT, MAXWIDTH), dtype='<U20')
        self.grid[:] = ' '

        for i in range(self.__columns):
            if(i%5==0):
                self.grid[8,i]=COIN

                
    def show_board(self, a):
        '''Shows grid from a of WIDTH width
        '''
        if a+WIDTH>MAXWIDTH:
            a=MAXWIDTH-WIDTH
        for i in range(self.__rows):
                for j in range(a, a+WIDTH):  # WIDTH columns at a time
                    print(self.grid[i][j], end='')
                print()

    def get_x(self):
        return self.__x

    def get_y(self):
        return self.__y