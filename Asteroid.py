import math
import pygame
from Bullet import Bullet
from Ship import Ship
import random

WIDTH = 500
HEIGHT = 500
BLACK = (0, 0, 0)

class Asteroid:
    
    def __init__(self, x=0, y=0, size=0, sf=0, alive=False, mode=1):
        self.x = x
        self.y = y
        self.size = size
        self.scale = sf
        self.alive = alive
        self.poly = []
        self.angle = 2*math.pi*random.uniform(0, 1)
        self.speed = random.uniform(0, 1)*2 + 1
        self.mode = mode
        self.construct_poly(mode)
    
    def construct_poly(self, mode):
        
        if mode == 0:
            smallR = 0.6
            bigR = 1
        
            for i in range(0, 10):
                ang = 2*math.pi*i/10
                dist = random.uniform(0,1)
                dist = dist*smallR + (bigR-smallR)
                self.poly.append((math.cos(ang)*dist*self.scale, math.sin(ang)*dist*self.scale))
        else:
            # Create hexagon
            for i in range(0, 10):
                ang = 2*math.pi*i/10
                self.poly.append((math.cos(ang)*self.scale, math.sin(ang)*self.scale))
            
    
    def circle_collision(self, x1, y1, r1, x2, y2, r2):
        distance = math.sqrt((x1-x2)**2 + (y1-y2)**2)
        return distance <= r1 + r2
    
    def bullet_collision(self, bullet):
        return self.circle_collision(self.x, self.y, self.scale, bullet.x, bullet.y, bullet.r)
        
            
    
    def ship_collision(self, ship):
        if self.mode == 0:
            return self.circle_collision(self.x, self.y, self.scale - self.scale/3.5, ship.posX, ship.posY, ship.scale/2)
        else:
            return self.circle_collision(self.x, self.y, self.scale, ship.posX, ship.posY, ship.scale/2)
    
    def draw(self, window):
        
        temp_poly = []
        for i in range(0, 10):
            temp_poly.append((self.poly[i][0] + self.x, self.poly[i][1] + self.y))
        pygame.draw.polygon(window, BLACK, temp_poly, 3)
    
    def move(self):
        self.x += self.speed*math.cos(self.angle)
        self.y += self.speed*math.sin(self.angle)
        
        if self.x > WIDTH + self.scale:
            self.x = -self.scale
        elif self.x < -self.scale:
            self.x = WIDTH + self.scale
        
        if self.y > HEIGHT + self.scale:
            self.y = -self.scale
        elif self.y < -self.scale:
            self.y = HEIGHT + self.scale
            
    def is_alive(self):
        return self.alive
        