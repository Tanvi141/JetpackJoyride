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
        self.__oldx=0
        self.__oldy=0

        self.__coins = 0
        self.__lives = 3
        self.__airtime = 0
        self.__shield = 0

        self.__score=0

    def get_x(self):
        return self.__x

    def get_y(self):
        return self.__y

    def get_coins(self):
        return self.__coins
    
    def change_score(self,val):
        self.__score+=val

    def get_score(self):
        return self.__score
    
    def get_lives(self):
        return self.__lives
    
    def kill_mando(self):
        self.__lives-=1

    def update_old(self):
        self.__oldx=self.__x
        self.__oldy=self.__y

    def get_shield(self):
        return self.__shield
    
    def set_shield(self,val):
        self.__shield=val

    def get_airtime(self):
        return self.__airtime
    
    def generate_shape(self):
        '''Gives Mando's body appropriate shape according to dirn and type of movement
        '''
        if self.__shield==0:
            if self.__fly == 1:
                self.__body[0] = [RED+'\\'+RESET, BLUE+'0'+RESET, RED+'/'+RESET]
                self.__body[1] = [' ', BLUE+Back.RED+' '+RESET, ' ']

            else:
                self.__body[0] = [' ', BLUE+'0'+RESET, ' ']
                self.__body[1] = [RED+'/'+RESET, BLUE +
                                Back.RED+' '+RESET, RED+'\\'+RESET]

            if self.__dirn == 0:
                self.__body[2] = [RED+'/'+RESET, ' ', RED+'\\'+RESET]

            elif self.__dirn == -1:
                self.__body[2] = [RED+'<'+RESET, ' ', RED+'\\'+RESET]

            else:
                self.__body[2] = [RED+'/'+RESET, ' ', RED+'>'+RESET]
        
        else:
            if self.__fly == 1:
                self.__body[0] = [Fore.WHITE+'\\'+RESET, Fore.WHITE+'0'+RESET, Fore.WHITE+'/'+RESET]
                self.__body[1] = [' ', Fore.WHITE+Back.BLACK+' '+RESET, ' ']

            else:
                self.__body[0] = [' ', Fore.WHITE+'0'+RESET, ' ']
                self.__body[1] = [Fore.WHITE+'/'+RESET,Fore.WHITE +
                                Back.BLACK+' '+RESET, Fore.WHITE+'\\'+RESET]

            if self.__dirn == 0:
                self.__body[2] = [Fore.WHITE+'/'+RESET, ' ', Fore.WHITE+'\\'+RESET]

            elif self.__dirn == -1:
                self.__body[2] = [Fore.WHITE+'<'+RESET, ' ', Fore.WHITE+'\\'+RESET]

            else:
                self.__body[2] = [Fore.WHITE+'/'+RESET, ' ', Fore.WHITE+'>'+RESET]

    def place_mando(self, grid,counterinc):
        '''Places the mando at appropriate position with torso at x,y and counts the coinss
        '''
        x = self.__x
        y = self.__y
        grid[y-1:y+2, x-1:x+2] = self.__body

    def erase_mando(self, grid,counter):
        '''Erases mando off the board, reduces lives
        '''
        x = self.__x
        y = self.__y
        grid[y-1:y+2, x-1:x+2] = self.__empty

    def set_values(self, x, dirn, fly, counter):
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
        ''' Time to calculate gravity drop
        '''
        if(self.__fly == 1 or self.__y == HEIGHT-GROUND-2):
            self.__airtime = 0

        else:
            self.__airtime += 1

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
    
    def check_coin(self,obj_coin,grid):
        if obj_coin.get_lives()==0:
            return 

        x_coin=obj_coin.get_x()
        y_coin=obj_coin.get_y()

        x_max=max(self.__x,self.__oldx)+1
        x_min=min(self.__x,self.__oldx)-1
        y_max=max(self.__y,self.__oldy)+1
        y_min=min(self.__y,self.__oldy)-1
        # print(x_min, x_max,x_coin, y_min, y_max,y_coin)

        if(x_coin<=x_max and x_coin>=x_min and y_coin<=y_max and y_coin>=y_min):
            self.__coins+=1
            obj_coin.erase_coin(grid)
            self.change_score(10)
            
        return 


