import pygame
from Ship import Ship
from AsteroidPool import AsteroidPool

# Window properties
WIDTH, HEIGHT = 500, 500
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Asteroids by Mladen")

# Frame rate
FPS = 30
ASTER_POOL_SIZE = 100
BLACK = (255, 255, 255)

def main():
    # game loop
    clock = pygame.time.Clock()
    run = True
    
    ship = Ship(WIN)
    keys = [False, False, False, False]
    
    aster_pool = AsteroidPool(WIN, ASTER_POOL_SIZE)
    
    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
        
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    keys[0] = True
                    
                if event.key == pygame.K_RIGHT:
                    keys[1] = True
                    
                if event.key == pygame.K_UP:
                    keys[2] = True
                
                if event.key == pygame.K_SPACE:
                    keys[3] = True
                    
                    
            
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT:
                    keys[0] = False
                    
                if event.key == pygame.K_RIGHT:
                    keys[1] = False
                    
                if event.key == pygame.K_UP:
                    keys[2] = False
                    ship.lastAngle = ship.angle
                
                if event.key == pygame.K_SPACE:
                    keys[3] = False
        
        if keys[0]:
            ship.rotate_left(0.1)
        if keys[1]:
            ship.rotate_right(0.1)
        if keys[2]:
            ship.move_forward()
            ship.update(ship.angle)
        else:
            ship.gas -= 0.02
            if ship.gas < 0:
                ship.gas = 0
            ship.update(ship.lastAngle)
        
        if keys[3]:
            ship.shoot()
         
        WIN.fill(BLACK)
        ship.render()
        
        aster_pool.bullet_collision_handler(ship.bullets)
        done = aster_pool.ship_collision_handler(ship)
        aster_pool.move_asteroids()
        aster_pool.draw_asteroids()
       
        if done:
            # need to reset game
            print("Episode is done.")
            break
        
        pygame.display.update()
        
        
    pygame.quit()
    

if __name__ == "__main__":
    main()
  
