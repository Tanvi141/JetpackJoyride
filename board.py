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
        self.grid=np.zeros((HEIGHT,MAXWIDTH),dtype='<U20')
        self.grid[:]=' '

    def show_board(self, a): 

        if(a > MAXWIDTH-WIDTH):  # the grid stops moving at end
            for i in range(self.__rows):
                for j in range(a,a+WIDTH):  # WIDTH columns at a time
                    print(self.grid[i][j], end='')
                print()

        else:  # grid instead of character moves, character in the middle
            for i in range(self.__rows):
                for j in range(MAXWIDTH-WIDTH,WIDTH):  # WIDTH columns at a time
                    print(self.grid[i][j], end='')
                print()
    

    def show_all(self): 
        
        for i in range(self.__rows):
            for j in range(self.__columns):  # WIDTH columns at a time
                print(self.grid[i][j], end='')
            print()
    
