import numpy as np
import cv2
from math import *
from random import randint
from numba import jit

XRES = 2**7
YRES = XRES
tx = 0.01


@jit(nopython=True)
def findForce(buff, ind):
    tx = 0
    ty = 0
    x = buff[5*ind]
    y = buff[5*ind+1]
    for i in range(int(len(buff) / 5)):
        bad = np.zeros((0))
        if i != ind:
            if (abs(x - buff[5*i]) < 0.01 and abs(y - buff[5*i+1]) < 0.01):
                pass

            else:
                ds = ((buff[5*i] - x)**2 + (buff[5*i+1] - y)**2)
                #print(ds)
                tf = 0.01*buff[5*i+4] * buff[5*ind+4]
                if (buff[5*i]-x) == 0:
                    theta = pi/2
                else:
                    theta = abs(atan((buff[5*i+1]-y)/(buff[5*i]-x)))
                if (x > buff[5*i] and y > buff[5*i+1]):
                    theta = pi+theta
                elif (y > buff[5*i+1]):
                    theta = -theta
                elif (x > buff[5*i]):
                    theta = pi-theta
                ty += sin(theta) * tf
                tx += cos(theta) * tf

                #print(tx,ty)


    return float(tx), float(ty), buff

@jit(nopython=True)
def updateBuffer(buff):
    for i in range(int(len(buff)/5)):
        x,y, buff = findForce(buff, i)
        m = buff[5*i+4]
        buff[5*i+2] +=  x / m
        buff[5*i+3] +=  y / m

        #buff[5*i+2] *= 0.9
        #buff[5*i+3] *= 0.9

        buff[5*i] += buff[5*i+2] * tx
        buff[5*i+1] += buff[5*i+3] * tx
    return buff

def drawBuffer(buff, src):
    for i in range(int(len(buff)/5)):
        y = int(buff[5*i+1])
        x =  int(buff[5*i])
        if (x > 1 and x < XRES-1) and (y > 1 and y < YRES-1):
            src[y,  x] += 1
            src[y-1,x] += 0.5
            src[y+1,x] += 0.5
            src[y,x-1] += 0.5
            src[y,x+1] += 0.5
    mx=np.amax(src)
    return src/10


def new(x,y,dx,dy,m, buff):
    buff = np.append(buff, x)
    buff = np.append(buff, y)
    buff = np.append(buff, dx)
    buff = np.append(buff, dy)
    buff = np.append(buff, m)

    return buff

#x, y = findForce([0,0,0,0,1,1,0,0,0,1,1,1,0,0,1],1)
buff = np.zeros((0))

for i in range(500):
    x,y = randint(0,XRES),randint(0,YRES)
    buff=new(x,y,(y-YRES/2),-(x-XRES/2),1,buff)

im = np.zeros((YRES, XRES)).astype('float32')

while True:
    #print(buff)
    #buff=new(randint(0,XRES),randint(0,YRES),0,0,1,buff)

    #im = np.zeros((YRES, XRES))
    im *= 0
    buff = updateBuffer(buff)
    im = drawBuffer(buff, im)
    resized = cv2.resize(im, (256,256), interpolation = cv2.INTER_AREA)
    cv2.imshow("fr", resized)
    cv2.waitKey(1)
