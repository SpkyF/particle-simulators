###ilovenukes
#from numba import jit
from math import sqrt, pi, cos, sin
import cv2
import numpy as np
import random

hits = 0#
#@jit
def distance(t1,t2):
    dx = t1[0] - t2[0]
    dy = t1[1] - t2[1]    #if dis < 1:
#        print(dx,dy,dis,end="\r")

    return sqrt((dx**2) + (dy**2))

bodies=[]
class neutron:
    def __init__(self,loc):
        self.type = -1
        self.location = loc
        self.speed = random.randint(5,500)
        angle = random.randint(0,360) * pi / 180
        self.velocity = (cos(angle)*self.speed,sin(angle)*self.speed)
        self.color = (1,1,1)
        bodies.append(self)
    def update(self):
        global grid
        try:
            grid[int (self.location[0]), int (self.location[1])] = self.color
        except:
            bodies.remove(self)

class uranium:
    def __init__(self,type,loc=(0,0)):
        self.location = loc
        self.type = type
        self.velocity = (0,0)
        self.speed = 0
        if type == 1:
            self.color = (0,1,0)
        else:
            self.color = (0.25,0.75,0.25)
        bodies.append(self)
    def hit(self):
        global hits
        bodies.remove(self)
        for j in range(3):
            neutron((self.location))
        hits += 1
        print(hits,end="\r")
    def update(self):
        global grid
        if self.type == 1:
            if random.randint(0,radioactivity) == 0:
                self.hit()
            else:
                for i in bodies:
                    dis = distance(i.location,self.location)
                    if ((dis <= 5) and (i.speed < 200) and (i.speed > 50) and i != self):
                        self.hit()
                        break
        try:
            grid[int (self.location[0]), int (self.location[1])] = (self.color)
        except:
            bodies.remove(self)
dt = 0.001
xmax = 100
ymax = 100
radioactivity = 10000


grid = np.zeros((xmax+1,ymax+1,3))

for i in range(300):
    uranium(1,loc=(random.randint(0,xmax),random.randint(0,ymax)))


while True:
    for i in bodies:
        i.location = (i.location[0]+i.velocity[0]*dt,i.location[1]+i.velocity[1]*dt)

        i.update()
    cv2.imshow('arr',grid)
    #cv2.waitKey(1)
    grid = np.zeros((xmax+1,ymax+1,3))

    if cv2.waitKey(1) == ord("q"):
        break
