
#import cProfile
import re

from math import sqrt, log
import numpy as np
import cv2
#cv2.namedWindow("output", cv2.WINDOW_NORMAL)
from random import randint



### TUNEABLES
#changing these constants gives different results, turning the coupling to 0 gives an ideal gas, turning the collision radius to a large value gives microscale repulsion, and changing the sign/magnetude of coupling gives results from charged gasses

c = 0.999 #decay, bounds particles to realistic speeds, i think about it as Bremsstrahlung radiation to justify it even if its not true
collision_radius = 5
do = 0.05
timestep = 0.01
res = (200,200)
buf = 1 #wall thickness buffer
v = 1000
temp = 10 #tempurature of bounding box
coupling = 100 #coupling const between particles
g=100
num_particles = 100

#@profile
def dop(x):
    if x != 0:
        return min(100,5+(8*(do*x)**2 - (do*x)**4)*4*2.71**(-do*x))#+ 1/(do*x)**2
    else:
        return 0

def tempuraturedelta(v, t):
    return np.random.normal(loc = (t - v), scale = 5, size = None) #simplistic thermal energy transfer


def collision(p1,p2):
    dx = p1.p[0] - p2.p[0]
    dy = p1.p[1] - p2.p[1]
    d = sqrt(dy**2 + dx**2)
    if d < 2 * collision_radius:
        v1 = p1.v
        v2 = p2.v
        x1 = p1.p
        x2 = p2.p
        if d != 0:
            p1.f = p1.f + coupling * (x1 - x2) * dop(d) / d
            p2.f = p2.f + coupling * (x2 - x1) * dop(d) / d
        else:
            p1.f = p1.f + coupling * (x1 - x2) * dop(d) / (d+1)
            p2.f = p2.f + coupling * (x2 - x1) * dop(d) / (d+1)
        #p1.p = p1.p + p1.v * timestep * 1
        if d < collision_radius: #avoids divide by zero error at close range by giving particles a random kick
            #p1.p = p1.p * randint(0,1000) / 1000
            pass
        #print(p1.v)


class Particle():
    #@profile
    def __init__(self,x,y,m=1,v=(0,0),r=1):
        self.p = np.array((x,y))
        self.v = np.array(v)
        self.m = m
        self.r = r
        self.f = np.array((0,0))
        particles.append(self)
    #@profile
    def update(self):
        self.v = self.v + timestep * self.f / self.m
        self.f = np.array((0,0))
        self.v[0] = self.v[0] + g * timestep
        #self.v = self.v * c
        self.p = self.p + timestep * self.v
        if (self.p[0] < buf):
            self.p[0] = 2 * buf
            self.v[0] = -self.v[0] * c
        elif (self.p[1] < buf):
            self.p[1] = 2 * buf
            self.v[1] = - self.v[1] * c
        elif (self.p[0] > res[0] - buf):
            self.p[0] = res[0] - 2 * buf
            self.v[0] = -self.v[0]*c - tempuraturedelta(sqrt(self.v[0]**2 + self.v[1]**2), temp)
            self.v[1] = self.v[1] / 2
        elif (self.p[1] > res[1] - buf):
            self.p[1] = res[1] - 2 * buf
            self.v[1] = -self.v[1] * c

        else:
            try:
                #frame[round(self.p[1]),round(self.p[0])] = 1
                cv2.circle(frame, (round(self.p[1]),round(self.p[0])),self.r-1,(1))
            except IndexError:
                pass


particles = []
#Particle(100,10,10,(10,10),10)
for i in range(num_particles):
    Particle(randint(buf,res[0] - buf),randint(buf,res[1] - buf),m=randint(1,1),v=(randint(-v,v),randint(-v,v)))
#k=1000
frame = np.zeros((res[1],res[0]))
while True:
    #k -= 1
    #if k == 0:
        #temp = 0.01
        #c=0.995
        #g=0

    frame = np.zeros((res[1],res[0]))
    l = len(particles)
    for i in range(l):
        for j in range(l-i):
            if i != l-j-1 and abs(particles[i].p[0] - particles[l-j-1].p[0]) < max(2*collision_radius,particles[i].r):
                collision(particles[i],particles[l-j-1])
        particles[i].update()
    cv2.imshow("output",frame)
    cv2.waitKey(1)
    #x,y,w,h = cv2.getWindowImageRect('output')
    #res  = (h,w)
    #res = (w-4,h-81)
print("done")
#cProfile.run('re.compile("gassim3.py")',sort="ncalls")
