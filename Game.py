import pygame
from Ship import Ship
from AsteroidPool import AsteroidPool
from PIL import Image
import numpy as np
from skimage.transform import resize


# Window properties
WIDTH, HEIGHT = 500, 500
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Asteroids by Mladen")

# Frame rate
FPS = 30
ASTER_POOL_SIZE = 100
WHITE = (255, 255, 255)

FRAME_SKIP = 4

ACT_LEFT  = [1, 0, 0, 0, 0, 0]
ACT_RIGHT = [0, 1, 0, 0, 0, 0]
ACT_UP    = [0, 0, 1, 0, 0, 0]
ACT_SHOOT = [0, 0, 0, 1, 0, 0]
ACT_LEFT_SHOOT = [0, 0, 0, 0, 1, 0]
ACT_RIGHT_SHOOT = [0, 0, 0, 0, 0, 1]

ROTATE_STEP = 0.1

class Game:
    
    def __init__(self):
        
        self.ship = Ship(WIN)
        self.aster_pool = AsteroidPool(WIN, ASTER_POOL_SIZE)
        self.actions = [ACT_LEFT, ACT_RIGHT, ACT_UP, ACT_SHOOT, ACT_LEFT_SHOOT, ACT_RIGHT_SHOOT]
        self.score = 0
        
    
    def play_step(self, action):
        
        screen1 = []
        screen2 = []
        screen3 = []
        screen4 = []
        
        reward = -0.01
        
        iter = 0
        while iter < FRAME_SKIP:
            
            if action != None:
                act_ind = self.actions.index(action)
        
                if self.actions[act_ind] == ACT_LEFT:
                    self.ship.rotate_left(ROTATE_STEP)
            
                elif self.actions[act_ind] == ACT_RIGHT:
                    self.ship.rotate_right(ROTATE_STEP)
            
        
                if self.actions[act_ind] == ACT_UP:
                    self.ship.move_forward()
                    #self.ship.update(self.ship.angle)
                #else:
                    # for now
                    #self.ship.gas -= 0.02
                    #if self.ship.gas < 0:
                        #self.ship.gas = 0
                    self.ship.gas = 0
                    #self.ship.update(self.ship.lastAngle)
                    
                if self.actions[act_ind] == ACT_LEFT_SHOOT:
                    self.ship.shoot()
                    self.ship.rotate_left(ROTATE_STEP)
                     
                if self.actions[act_ind] == ACT_RIGHT_SHOOT:
                    self.ship.shoot()
                    self.ship.rotate_right(ROTATE_STEP)
        
                if self.actions[act_ind] == ACT_SHOOT:
                    self.ship.shoot()
                
                #UPDATE?
                self.ship.update(self.ship.angle)            
            
            WIN.fill(WHITE)
        
            self.ship.render()
            
            temp_reward = self.aster_pool.bullet_collision_handler(self.ship.bullets)/25
            reward += temp_reward
            self.score += temp_reward
            done = self.aster_pool.ship_collision_handler(self.ship)
            self.aster_pool.move_asteroids()
            self.aster_pool.draw_asteroids()
        
            pygame.display.update()
            
            min_distance = self.aster_pool.min_distance(self.ship)
            if min_distance > 50:
                reward += 0.2
              
            if done:
                # need to reset game
                print("Episode is done.")
            
            # Saving only RED Color
            if iter == 0:
                screen1 = pygame.surfarray.array_red(WIN)
            if iter == 1:
                screen2 = pygame.surfarray.array_red(WIN)
            if iter == 2:
                screen3 = pygame.surfarray.array_red(WIN)
                
            iter += 1
        
        
        #save 4'th image
        screen4 = pygame.surfarray.array_red(WIN)
        
    
        screen1 = resize(screen1, (84, 84))
        screen2 = resize(screen2, (84, 84))
        screen3 = resize(screen3, (84, 84))
        screen4 = resize(screen4, (84, 84))
                   
        state = np.stack((screen1, screen2, screen3, screen4), axis=2)
        
        
        if done:
            reward = -1
        
        return (state, reward, done, self.score)
            
    
    def reset(self):
        self.ship = Ship(WIN)
        self.aster_pool = AsteroidPool(WIN, ASTER_POOL_SIZE)
        self.score = 0        
    