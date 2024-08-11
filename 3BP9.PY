import cv2
import numpy as np
from math import *
from random import randint
from numba import jit

YRES = 600
XRES = 2*YRES
dt = 1
g = 500
c = 12000
ccf = 200

mass = []
xpos = []
ypos = []
vx = []
vy = []
def floorl(l):
    l = [floor(i) for i in l]
    return l

def newMass(x,y,vxp=0,vyp=0,m=1):
    xpos.append(x)
    ypos.append(y)
    vx.append(vxp)
    vy.append(vyp)
    mass.append(m)

def delmass(i):
    xpos.pop(i)
    ypos.pop(i)
    vx.pop(i)
    vy.pop(i)
    mass.pop(i)


def idis2(dx,dy):
    d = dx**2 + dy**2
    f=0
    if d > 0:
        f = 1/d - 0.125/((d-ccf)**2)
    if d > ccf**2:
        return f
    return 0.000001*f

def calcf(x1,y1,x2,y2,m1,m2):
    dx = x2-x1
    dy = y2-y1
    f = m1 * m2 * idis2(dx,dy)
    fx = g*f*sin(atan2(dx,dy))
    fy = g*f*cos(atan2(dx,dy))
    return fx, fy

for i in range(100):
    newMass(randint(0,XRES-1),randint(0,YRES-1),randint(-5,5),randint(-5,5),10)
newMass(XRES/2,YRES/2,0,0,100)

while True:
    #newMass(randint(0,XRES-1),randint(0,YRES-1))
    #if randint(0,20) == 0:
        #delmass(randint(0,len(xpos)-1))
        #newMass(randint(0,XRES-1),randint(0,YRES-1),randint(-5,5),randint(-5,5))

    arr = np.zeros((YRES,XRES))
    for i in range(len(xpos)):
        try:
            v = sqrt(vx[i]**2 + vy[i]**2)
        except:
            delmass(i)
            newMass(randint(0,XRES-1),randint(0,YRES-1),randint(-5,5),randint(-5,5))

        gc = abs(1 - abs(v / c))
        vx[i] *= gc
        vy[i] *= gc
        fx = 0
        fy = 0
        for j in range(len(xpos)):
            if j != i:
                fx1, fy1 = calcf(xpos[i],ypos[i],xpos[j],ypos[j],mass[i],mass[j])
                fx += fx1
                fy += fy1
        vx[i] += fx / mass[i]
        vy[i] += fy / mass[i]
    for i in range(len(xpos)):
        xpos[i] += vx[i] * dt
        ypos[i] += vy[i] * dt
        if xpos[i] >= (XRES-1):
            xpos[i] = 1
        if xpos[i] <= 0:
            xpos[i] = XRES - 2
        if ypos[i] >= (YRES-1):
            ypos[i] = 1
        if ypos[i] <= 0:
            ypos[i] = YRES - 2

    #arr[floorl(ypos),floorl(xpos)] = 1
    for i in range(len(ypos)):
        cv2.circle(arr,(floor(xpos[i]),floor(ypos[i])),floor(log(mass[i])),1,-1)
    cv2.imshow("Ar",arr)
    cv2.waitKey(1)
