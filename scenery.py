from headerfile import *
import numpy as np


class Scenery:

    def __init__(self):
        self.__skyblockwidth = 2
        self.__groundblockwidth = 2
        self.__groundblock = np.array([[Fore.LIGHTGREEN_EX+Back.LIGHTBLACK_EX + '-'+RESET, Fore.LIGHTGREEN_EX+Back.LIGHTBLACK_EX + '-'+RESET], [
                                      GCOLOR+'_'+RESET, GCOLOR+'w'+RESET], [GCOLOR+'_'+RESET, GCOLOR+'w'+RESET]])
        self.__skyblock = np.array([[CYAN+'.'+RESET, CYAN+'\''+RESET], [
                                   CYAN+'\''+RESET, CYAN+'.'+RESET], [CYAN+'.'+RESET, CYAN+'\''+RESET]])

    def create_ground(self, grid):
        grid[HEIGHT-GROUND:HEIGHT,
             0:MAXWIDTH] = np.tile(self.__groundblock, (int)(MAXWIDTH/2))

    def create_sky(self, grid):
        grid[0:SKY,
             0:MAXWIDTH] = np.tile(self.__skyblock, (int)(MAXWIDTH/2))
