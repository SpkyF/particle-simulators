from math import *
import cv2
import numpy as np
import time
import random
from numba import jit
bodies = []
white= (1,1,1)

@jit
def grav(mass, grav, dist,dx,dy):
    ft = mass * grav / (dist**2)
    fx = dx * ft / dist
    fy = dy * ft / dist
    return fx, fy

@jit
def strongf(mass, sf, dist,dx,dy):
    dist2 = dist / sr
    ft = exp(-dist2)/(dist2**2) - 1/(dist**4)
    ft *= mass
    fx = s * dx * ft / dist
    fy = s * dy * ft / dist
    return fx, fy

def cmult(tup,const):
    tup = (tup[0] * const, tup[1] * const, tup[2] * const)
    return tup

def tmult(tup1,tup2):
    ls=[]
    for k in len(tup1):
        ls.append(tup1[k]*tup2[k])
    return tuple(ls)

def ofset(xy,of):
    return(xy[0]+of[0],xy[1]+of[1])

def ofset2(xy,of):
    return(xy[0]+of[0],xy[1]+of[1],xy[2]+of[2])

def roundtup(xy):
    return (round(xy[0]),round(xy[1]))

def distance(xy):
    dx=xy[0]
    dy=xy[1]
    dis = sqrt(dx**2 + dy**2)
    return dis

class particle:
    def __init__(self,location,mass=1,velocity=(0,0),color=white):
        bodies.append(self)
        self.mass=mass
        self.velocity = (0,0)
        self.location = location
        self.velocity = ofset(velocity,(-10*self.location[1]/abs(self.location[1]+0.01),10*self.location[0]/abs(self.location[0]+0.01)))
        self.velocity = ofset(velocity,(-ls*self.location[0],-ls*self.location[1]))
        self.rad = round(log(self.mass,10)+1)
        self.color = color

    def updatevel(self):
        forcex=0
        forcey=0
        for i in bodies:
            if i!=self:
                dx=i.location[0]-self.location[0]
                dy=i.location[1]-self.location[1]
                ds=distance((dx,dy))
                if ds < (i.rad + self.rad):
                    self.collision(i)
                    break
                    #print('heyo!')
                fx,fy = grav(i.mass,g,ds,dx,dy)
                forcex += fx
                forcey += fy

                fx,fy =strongf(i.mass,s,ds,dx,dy)
                forcex += fx
                forcey += fy

        self.velocity = (damping*self.velocity[0] + forcex,damping*self.velocity[1] + forcey)

    def update(self):
        self.location = (self.location[0] + self.velocity[0]*dt,self.location[1] + self.velocity[1]*dt)
        return cv2.circle(plt,roundtup(ofset(ofset(self.location,(dim[1]/2,dim[0]/2)),centerofmass)),self.rad,self.color,-1)
    def dels(self):
        try:
            bodies.remove(self)
        except:
            pass

    def collision(self,other):
        other.velocity = ((other.velocity[0]*other.mass + self.velocity[0] * self.mass)/(other.mass+self.mass),(other.velocity[1]*other.mass + self.velocity[1] * self.mass)/(other.mass+self.mass))
        other.color = ofset2(cmult(other.color,other.mass),cmult(self.color,self.mass))
        other.mass += self.mass
        other.color = (other.color[0]/other.mass,other.color[1]/other.mass,other.color[2]/other.mass)
        other.rad=round(log(other.mass,10)+1)
        #self.rad=other.rad
        self.dels()
        #quit()
centerofmass=(0,0)
totalmass = 0

g=2
c=1
s=-1
dt=0.05
sr=5
damping=1
ls=0.1

dim=(800,1500,3)
plt=np.zeros(dim)
trails = plt

mxrange=2*distance((dim[0],dim[1]))
#particle((0,25),velocity=(0,0),mass=1000)
#particle((0,-25),velocity=(0,0),mass=1001)
#particle((25,0),velocity=(0,0),mass=1001)
particle((0,0),velocity=(0,0),mass=1000)

for i in range(200):
    particle((random.randint(0,dim[1])-dim[1]/2,random.randint(0,dim[0])-dim[0]/2),velocity=(random.randint(0,2)-1,random.randint(0,2)-1),mass=random.randint(1,5),color=(random.randint(1,255)/255,random.randint(1,255)/255,random.randint(1,255)/255))
ls=1.5
while True:

    if len(bodies) < 50:
        particle((random.randint(0,dim[0])-dim[0]/2,random.randint(0,dim[1])-dim[1]/2),mass=random.randint(1,5),color=(random.randint(1,255)/255,random.randint(1,255)/255,random.randint(1,255)/255))

    biggestmass=0
    #p.rad=3
    for i in bodies:
        if abs(i.location[0]) > 2*dim[0] or abs(i.location[1]) > 2 * dim[1]:
            bodies.remove(i)
        if i.mass > biggestmass:
            biggestmass = i.mass
    for i in bodies:
        if i.mass == biggestmass:
            centerofmass = (-i.location[0],-i.location[1])
            break
    for i in bodies:
        i.updatevel()
    for i in bodies:
        plt=i.update()
    #plt = cv2.circle(plt,roundtup(ofset((dim[1]/2,dim[0]/2),centerofmass)),10,(0,0,1),-1)
    plt=cv2.circle(plt,roundtup(ofset((dim[1]/2,dim[0]/2),centerofmass)),round(mxrange),(0,0,1),2)
    #trails += plt
    #trails *= 0.99
    cv2.namedWindow("plt", cv2.WND_PROP_FULLSCREEN)
    cv2.setWindowProperty("plt",cv2.WND_PROP_FULLSCREEN,cv2.WINDOW_FULLSCREEN)
    cv2.imshow('plt',plt)

    #time.sleep(dt)
    plt=np.zeros(dim)
    if cv2.waitKey(1)==ord("q"):
        break
    if cv2.waitKey(1)==ord("l"):
        for i in bodies:
            if i.mass == biggestmass:
                bodies.remove(i)
