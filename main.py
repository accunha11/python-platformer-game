import pygame
import constants

pygame.init()
pygame.display.set_caption("Platformer")
window = pygame.display.set_mode((constants.WIDTH, constants.HEIGHT))

from sprites import Block, Box, Player, Flag, Fire, Fruit, Score
from helper_functions import get_background, draw, handle_move
from levels.level1 import level1

def main(window):
    clock = pygame.time.Clock()
    background, bg_image = get_background("Blue.png")

    player = Player(constants.WIDTH // 2 - 50, constants.HEIGHT - constants.BLOCK_SIZE, 50, 50)
    player.direction = "right"
    floor = [Block(i * constants.BLOCK_SIZE, constants.HEIGHT - constants.BLOCK_SIZE, constants.BLOCK_SIZE) 
             for i in range(0, (constants.WIDTH * 2) // constants.BLOCK_SIZE)]
    
    objects = [*floor]

    run = True
    while run:
        clock.tick(constants.FPS) #regulate frame rate across different devices

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break
                
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                   level1(window)
        
        player.loop(constants.FPS)
        handle_move(player, objects, True)
        draw(window, background, bg_image, player, objects)

    pygame.quit()
    quit()


if __name__ == "__main__":
    main(window)