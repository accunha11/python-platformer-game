import pygame
from helpers.constants import *

from sprites.objects import *
from screens.final_score import *
from helpers.helper_functions import get_background, draw, handle_move


def game_over(window, player, old_objects, loopable_obj, offset_x):
    clock = pygame.time.Clock()
    background, bg_image = get_background("Blue.png")

    objects = [*old_objects]

    initial_time = pygame.time.get_ticks()

    run = True
    while run:
        clock.tick(FPS)  # regulate frame rate across different devices

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and player.jump_count < 2:
                    player.jump()

        player.loop()

        for loop in loopable_obj:
            loop.loop()

        for obj in objects:
            obj.trigger_gravity(HEIGHT * 2)
        
        if (pygame.time.get_ticks() - initial_time) > 1000:
            final_score(window, player.score)
            break

        handle_move(player, objects)
        draw(window, background, bg_image, [player], objects, offset_x)

    pygame.quit()
    quit()
