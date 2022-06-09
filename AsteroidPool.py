import math
import random
import pygame
from Asteroid import Asteroid
from Bullet import Bullet
from Ship import Ship

class AsteroidPool:
    
    def __init__(self, window, size):
        self.window = window
        self.size = size
        self.asters = []
        for i in range(size):
            self.asters.append(Asteroid())
        self.level = 1
        
        self.generate_new_level(1)
    
    def draw_asteroids(self):
        for i in range(0, self.size):
            if self.asters[i].is_alive():
                self.asters[i].draw(self.window)
    
    def move_asteroids(self):
        for i in range(0, self.size):
            if self.asters[i].is_alive():
                self.asters[i].move()
    
    def all_clear(self):
        for i in range(0, self.size):
            if self.asters[i].is_alive(): return False
        return True
    
    def add_asteroid(self, aster):
        for i in range(0, self.size):
            if not self.asters[i].is_alive():
                self.asters[i] = aster
                break
    
    def distance(self, x1, y1, x2, y2):
        return math.sqrt((x1 - x2)**2 + (y1 - y2)**2)
    
    def min_distance(self, ship):
        min_distance = 10000
        for i in range(0, self.size):
            if not self.asters[i].is_alive(): continue
            temp_distance = self.distance(ship.posX, ship.posY, self.asters[i].x, self.asters[i].y) + self.asters[i].scale
            if min_distance > temp_distance:
                min_distance = temp_distance
                
        return min_distance
    
    def bullet_collision_handler(self, bullets):
        reward = 0
        for i in range(0, self.size):
            if not self.asters[i].is_alive(): continue
            
            for j in range(len(bullets)):
                if bullets[j].is_gone(): continue
                if self.asters[i].bullet_collision(bullets[j]):
                    # Update pool, score, etc...
                    self.asters[i].alive = False
                    bullets[j].distance = 1000
                    reward += 50
                    
                    if self.asters[i].size == 1:
                        if self.all_clear():
                            # generate new level
                            self.level += 1
                            self.generate_new_level(self.level)
                        # dont add childs
                        continue
                    
                    # add childs
                    child1 = Asteroid(self.asters[i].x, self.asters[i].y, self.asters[i].size - 1, self.asters[i].scale/2, True)
                    child2 = Asteroid(self.asters[i].x, self.asters[i].y, self.asters[i].size - 1, self.asters[i].scale/2, True)
                    self.add_asteroid(child1)
                    self.add_asteroid(child2)
                    
                    return reward
                    
        return reward

                    
    def ship_collision_handler(self, ship):  
        for i in range(self.size):
            if self.asters[i].ship_collision(ship):
                return True
        return False
    
    def generate_new_level(self, level):
        aster_num = level*2
        for i in range(aster_num):
            ang = random.uniform(0, 1)*2*math.pi
            self.add_asteroid(Asteroid(400 + 400*math.cos(ang), 400 + 400*math.sin(ang), 3, 100, True))
        
        
        
        