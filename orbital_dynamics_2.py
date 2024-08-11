import math
import time
import pygame
import vectormath as vmath


bodies=[]
timestep=0.001
h,w=700,1000
c=155
grav=1

def gamma(v):
    try:
        g=1/math.sqrt(1-((v**2)/(c**2)))
    except:
        g=1

        #return float('inf')
    return g
offset = vmath.Vector2(w/2,h/2)


pygame.init()

pSurface = pygame.Surface((h,w))
mainDisplay = pygame.display.set_mode((w,h))

class planet:
    def __init__(self,mass,location,velocity,color=(150,255,150)):
        self.velocity=vmath.Vector2(velocity)
        self.location=vmath.Vector2(location)
        self.mass=mass
        bodies.append(self)
        self.color=color
    def __del__(self):
        #pass
        bodies.remove(self)
        #quit()

    def update(self,show=False):
        fnet=vmath.Vector2(0,0)
        g=gamma(self.velocity.length)
        ke=g*self.mass*self.velocity.length**2
        if show:
            print(g,end="\r")
        for i in bodies:
            if i != self:
                fnet += grav*(i.location-self.location).normalize()*(i.mass*self.mass/(i.location-self.location).length**2)
                #time.sleep(0.5)

        #print(g,end="\r")
        self.velocity+=fnet*timestep/(self.mass*g)
        v=self.velocity.length
        if v >= c:
            #time.sleep(0.1)
            #print('\n')
            print("relativistic limits broken")
            vel=self.velocity
            mass=self.mass
            loc=self.location
            self.__del__()
            return (vel*mass,loc,mass)
            #quit(1)
            vc=255
        else:
            vc=v*255/c
            self.color=(vc,255-vc,255-vc,)
            self.location+=self.velocity*timestep
            return 0

p1=planet(10000,(0,0),(-3,-3))
p2=planet(10000,(0,100),(3,3))
#p3=planet(100000,(-100,0),(-5,1))
#p4=planet(1,(0,-100),(1,1))

t=1000

while True:
    pSurface.fill((0,0,0))
    #time.sleep(timestep/t)
    for j in range(100):
        totaloffset = vmath.Vector2(0,0)
        totalmass=0
        for i in bodies:
            totaloffset += i.location#*i.mass
            totalmass += i.mass
        totaloffset *= 1/(len(bodies))
        #totaloffset *= 1/totalmass
        totaloffset=offset-totaloffset
        for i in bodies:
            i.update()



        #print(i.locaton)
    for i in bodies:
        pygame.draw.circle(pSurface,(50,50,50),(i.location+totaloffset),(i.mass*grav/(c**2)))
        pygame.draw.circle(pSurface,(i.color),(i.location+totaloffset),10)
    #totaloffset = vmath.Vector2(0,0)
    pygame.Surface.blit(mainDisplay,pSurface,(0,0))
    pygame.display.update()
    pygame.event.get()
