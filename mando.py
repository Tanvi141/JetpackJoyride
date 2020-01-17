import numpy as np
from headerfile import *


class Mando:
    '''Define the mando
    '''

    def __init__(self, dirn, fly):
        self.__x = PLACEWIDTH  # x coordinate of the torso
        self.__y = HEIGHT-GROUND-2  # y coordinate of the torso
        self.__dirn = dirn  # -1 means left, 0 means stop, 1 means right
        self.__fly = fly    # 1 means flying, 0 means not

        self.__body = np.zeros((3, 3), dtype='<U20')
        self.__body[:] = ' '
        # creating an empty array to make erasing easier
        self.__empty = np.zeros((3, 3), dtype='<U20')
        self.__empty[:] = ' '

        self.coins = 0
        self.lives = 3
        self.airtime = 0

    def get_x(self):
        return self.__x

    def get_y(self):
        return self.__y

    def generate_shape(self):
        '''Gives Mando's body appropriate shape according to dirn and type of movement
        '''
        if self.__fly == 1:
            self.__body[0] = [RED+'\\'+RESET, BLUE+'0'+RESET, RED+'/'+RESET]
            self.__body[1] = [' ', BLUE+Back.BLUE+'|'+RESET, ' ']

        else:
            self.__body[0] = [' ', BLUE+'0'+RESET, ' ']
            self.__body[1] = [RED+'/'+RESET, BLUE +
                              Back.BLUE+'|'+RESET, RED+'\\'+RESET]

        if self.__dirn == 0:
            self.__body[2] = [RED+'/'+RESET, ' ', RED+'\\'+RESET]

        elif self.__dirn == -1:
            self.__body[2] = [RED+'<'+RESET, ' ', RED+'\\'+RESET]

        else:
            self.__body[2] = [RED+'/'+RESET, ' ', RED+'>'+RESET]

    def place_mando(self, grid):
        '''Places the mando at appropriate position with torso at x,y and counts the coinss
        '''
        x = self.__x
        y = self.__y
        m = grid[y-1:y+2, x-1:x+2]
        self.coins += np.count_nonzero(m == COIN)
        grid[y-1:y+2, x-1:x+2] = self.__body

    def erase_mando(self, grid):
        '''Erases mando off the board, reduces lives
        '''
        x = self.__x
        y = self.__y
        grid[y-1:y+2, x-1:x+2] = self.__empty

    def set_values(self, x, dirn, fly, counter, grid):
        '''sets appropriate values of mando and returns 1 if in path of obstacle 
        '''
        # if any parameter is passed as -100 that means it should remain unchanged

        if x != -100:
            self.__x += x

            # don't change x coordinate if leaving the current screen
            if self.__x > counter+WIDTH-4:
                self.__x = counter+WIDTH-4
            elif self.__x < counter+3:
                self.__x = counter+3

        if dirn != -100:
            self.__dirn = dirn

        if fly != -100:
            self.__fly = fly

       

    def set_airtime(self):
        
        if(self.__fly == 1 or self.__y == HEIGHT-GROUND-2):
            self.airtime=0

        else:
            self.airtime+=1
    

    def change_y_mando(self):
    # now move him up or down according to the fly flag
        if self.__fly == 1 and self.__y > SKY+1:
            self.__y -= 2
            if self.__y < SKY+1:
                self.__y = SKY+1

        elif (self.__fly == 0) and self.__y < HEIGHT-GROUND-2:
            self.__y += 1
            if self.__y > HEIGHT-GROUND-2:
                self.__y = HEIGHT-GROUND-2