import math

BULLET_MAX_DISTANCE = 500


class Bullet:
    def __init__(self, x, y, r, speed, angle):
        self.x = x
        self.y = y
        self.r = r
        self.speed = speed
        self.angle = angle
        
        self.distance = 0
        
    def is_gone(self):
        return self.distance > BULLET_MAX_DISTANCE
    
    def move_bullet(self):
        self.x += self.speed*math.cos(self.angle)
        self.y += self.speed*math.sin(self.angle)
        
        self.distance += 10
        
