import pygame
import math
import time
import vectormath as vmath

timestep=0.001

display_width=1000
display_height=1000
c=200

count=0
count=1

offset = vmath.Vector2(display_width/2,display_height/2)


objects = []

class planet:
    def __init__(self, mass, location, velocity):
        self.mass = mass
        self.location = vmath.Vector2(location)
        self.velocity = vmath.Vector2(velocity)
        objects.append(self)

    def planet_update(self):
        fnet=vmath.Vector2(0,0)
        for i in objects:
            if i != self:
                fnet+=i.mass*self.mass/(i.location-self.location).length**2
                try:
                    bsmass=1/math.sqrt(1-((self.velocity.length**2)/(c**2)))

                except:
                    #bsmass=0
                    #print("Reletavistic Limits broken",end="\r")
                    #count+=1
                    pass
                #quit()
                try:
                    self.velocity=self.velocity+((fnet/bsmass)*(i.location-self.location).normalize())
                except:
                #count+=1
                    #print("Reletavistic Limits broken")
                    pass
            #print(a ,end="\r")
            self.location = self.location + self.velocity*timestep
class gravsource:
    def __init__(self, mass, location):
        self.mass = mass
        self.location = vmath.Vector2(location)
        #self.velocity = vmath.Vector2(velocity)
        objects.append(self)
    def planet_update(self):
        pass




#p1 = planet(10, (100,0), (-5,10))
p2 = planet(1, (100,0), (0,-50))
p3 = gravsource(1000,(0,0))

pygame.init()
mainDisplay = pygame.display.set_mode((display_width,display_height))
planetSurface = pygame.Surface((display_width,display_height))
trackingSurface = pygame.Surface((display_width,display_height))


while True:
    #time.sleep(timestep)
    for i in objects:
        i.planet_update()
        try:
            if i.velocity.length > c:
                pygame.draw.circle(planetSurface,(50,50,50),i.location+offset,10)
                pygame.draw.circle(trackingSurface,(250,250,250),i.location+offset,10)

            else:
                pygame.draw.circle(planetSurface,(155*i.velocity.length/c+100,100,100),i.location+offset,10)
                pygame.draw.circle(trackingSurface,(155*i.velocity.length/c+100,100,100),i.location+offset,10)

        except:
            pygame.draw.circle(planetSurface,(200,200,200),i.location+offset,10)

    pygame.Surface.blit(mainDisplay,planetSurface,(0,0))
    #pygame.Surface.blit(mainDisplay,trackingSurface,(0,0))
    pygame.display.update()
    pygame.event.get()
    pygame.Surface.fill(planetSurface,(0,0,0))

