import os
from colorama import Fore, init,Back, Style
init()

DEBUG = 'a'
# sizes
HEIGHT = 40
MAXWIDTH = 600
WIDTH = 150
PLACEWIDTH = 40
SKY = 3
GROUND = 3

# colors
RESET = Style.RESET_ALL
GREY = Fore.LIGHTBLACK_EX
CYAN = Fore.LIGHTCYAN_EX+Back.CYAN  
RED = Fore.BLUE
BLUE = Fore.BLUE
GCOLOR = Fore.LIGHTGREEN_EX+Back.GREEN
WHITE=Fore.WHITE
ICE=Fore.CYAN


# misc
COIN = Fore.LIGHTYELLOW_EX+'$'+Fore.RESET
STAR = Fore.RED+'w'+Style.RESET_ALL
