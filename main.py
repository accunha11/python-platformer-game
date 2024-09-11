import pygame
from helpers.constants import *

pygame.init()
pygame.display.set_caption("Platformer")
window = pygame.display.set_mode(( WIDTH,  HEIGHT))

from sprites.objects import Block
from sprites.player import Player
from helpers.helper_functions import get_background, draw, handle_move
from levels.level1 import level1

def main(window):
    clock = pygame.time.Clock()
    background, bg_image = get_background("Blue.png")

    player = Player( WIDTH // 2 - 50,  HEIGHT -  BLOCK_SIZE, 50, 50)
    player.direction = "right"
    floor = [Block(i *  BLOCK_SIZE,  HEIGHT -  BLOCK_SIZE,  BLOCK_SIZE) 
             for i in range(0, ( WIDTH * 2) //  BLOCK_SIZE)]
    
    objects = [*floor]

    run = True
    while run:
        clock.tick( FPS) #regulate frame rate across different devices

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break
                
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                   click_pos = pygame.mouse.get_pos()
                   if player.clicked(click_pos):
                       level1(window)
        
        player.loop( FPS)
        handle_move(player, objects, True)
        draw(window, background, bg_image, player, objects)

    pygame.quit()
    quit()


if __name__ == "__main__":
    main(window)