import pygame
import math
from Bullet import Bullet

BLACK = (0, 0, 0)
WIDTH = 500
HEIGHT = 500
MAX_BULLETS = 100
BULLET_GEN_TIME = 5

class Ship:
    def __init__(self, window):
        self.window = window
        self.posX = WIDTH/2
        self.posY = HEIGHT/2
        self.angle = 0
        self.lastAngle = 0
        self.thickness = 3
        self.scale = 25
        self.maxSpeed = 5
        self.gas = 0
        
        self.bPtr = 0
        self.bGenTime = 0
        self.bullets = []
    
    
    def rotate(self, origin, point, angle):
        ox, oy = origin
        px, py = point
        
        qx = ox + math.cos(angle) * (px - ox) - math.sin(angle) * (py - oy)
        qy = oy + math.sin(angle) * (px - ox) + math.cos(angle) * (py - oy)
        return qx, qy
    
    
    def render(self):
        seg1_start = self.rotate((self.posX, self.posY), (-0.5*self.scale + self.posX, -0.5*self.scale + self.posY), self.angle)
        seg1_end = self.rotate((self.posX, self.posY), (0 + self.posX, 0.5*self.scale + self.posY), self.angle)

        seg2_start = self.rotate((self.posX, self.posY), (0*self.scale + self.posX, 0.5*self.scale + self.posY), self.angle)
        seg2_end = self.rotate((self.posX, self.posY), (0.5*self.scale + self.posX, -0.5*self.scale + self.posY), self.angle)
        
        seg3_start = self.rotate((self.posX, self.posY), (-0.25*self.scale + self.posX, 0 + self.posY), self.angle)
        seg3_end = self.rotate((self.posX, self.posY), (0.25*self.scale + self.posX, 0 + self.posY), self.angle)
        
        pygame.draw.line(self.window, BLACK, seg1_start, seg1_end, self.thickness)
        pygame.draw.line(self.window, BLACK, seg2_start, seg2_end, self.thickness)
        pygame.draw.line(self.window, BLACK, seg3_start, seg3_end, self.thickness)
        
        # Draw and move bullets
        for b_ind in range(0, len(self.bullets)):
            bullet = self.bullets[b_ind]
            if not bullet.is_gone():
                bullet.move_bullet()
                pygame.draw.circle(self.window, BLACK, (bullet.x, bullet.y), bullet.r)
                
    
    def shoot(self):
        
        if self.bGenTime != 0:
            return
        
        if len(self.bullets) < 100:
            self.bullets.append(Bullet(self.posX + 10*math.cos(self.angle + math.pi/2), self.posY + 10*math.sin(self.angle + math.pi/2), 3, 10, self.angle + math.pi/2))
            
        else:
            self.bullets[self.bPtr % MAX_BULLETS] = Bullet(self.posX + 10*math.cos(self.angle + math.pi/2), self.posY + 10*math.sin(self.angle + math.pi/2), 3, 10, self.angle + math.pi/2)
            
        self.bPtr += 1
        self.bGenTime = BULLET_GEN_TIME
        
    def move_forward(self):
        self.gas += 0.05
        if self.gas > 1:
            self.gas = 1
            
    def rotate_left(self, ang):
        self.angle += -ang
    
    def rotate_right(self, ang):
        self.angle += ang
    
    def speed_function(self):
        fmax = 10
        return 0.5*(math.log10((self.gas*fmax)+0.1) + 1)
    
    # angle can be last angle
    def update(self, angle):
        self.posX += self.maxSpeed*self.speed_function()*math.cos(angle + math.pi/2)
        self.posY += self.maxSpeed*self.speed_function()*math.sin(angle + math.pi/2)
        
        
        if self.bGenTime > 0:
            self.bGenTime -= 1
        
        
        if self.posX > WIDTH:
            self.posX = 0
        
        if self.posX < 0:
            self.posX = WIDTH
            
        if self.posY > HEIGHT:
            self.posY = 0
        
        if self.posY < 0:
            self.posY = HEIGHT
        
        
    