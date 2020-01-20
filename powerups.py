import numpy as np
from headerfile import *
import time


class PowerUp():

    def __init__(self, recharge_time, active_time):
        self._activated = 0
        self._charged = 1
        self._recharge_time = recharge_time
        self._active_time = active_time
        self._recharge_track = 0
        self._active_track = 0

    def activate(self):  # change color on shield activation
        '''Activates only if it is charged and not active'''
        if self._charged == 1 and self._activated == 0:
            self._activated = 1
            self._charged = 0
            self._active_track = time.time()

    def status(self):
        if (self._activated == 1):
            return "Active"

        elif (self._charged == 0):
            return "Charging " + str(self._recharge_time-round(time.time() - self._recharge_track))

        else:
            return "Charged"


class SpeedBoost(PowerUp):

    def update(self, obj_mando):
        if obj_mando.get_x() > MAXWIDTH-WIDTH:
            self._activated = 0

        if self._activated == 1:
            if(time.time()-self._active_track > self._active_time):
                self._activated = 0
                self._recharge_track = time.time()
            return 4

        elif self._charged == 0:
            if (time.time()-self._recharge_track > self._recharge_time):
                self._charged = 1
        return 1


class Shield(PowerUp):

    def update(self, obj_mando):
        if self._activated == 1:
            if(time.time()-self._active_track > self._active_time):
                self._activated = 0
                self._recharge_track = time.time()
            obj_mando.shield = 1

        else:
            obj_mando.shield = 0
            if self._charged == 0:
                if (time.time()-self._recharge_track > self._recharge_time):
                    self._charged = 1
