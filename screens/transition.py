import pygame
from helpers.constants import *

from sprites.objects import *
from helpers.helper_functions import get_background, draw, handle_move
from levels.level1 import level1

def transition(window, player, old_objects, players):
    clock = pygame.time.Clock()
    background, bg_image = get_background("Blue.png")

    start_flag = Start_Flag(BLOCK_SIZE * 8, 0, 64)

    objects = [*old_objects, start_flag]

    offset_x = 0

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
        start_flag.loop()

        if player.rect.right >= WIDTH:
            player.frozen = True
            level1(window, player, start_flag, offset_x)
            break

        for pl in players:
            if pl.rect.y < 2*HEIGHT:
                pl.loop()
                pl.pass_through = True
                handle_move(player, objects)

        for obj in objects:
            if(obj.name == "start_flag"):
                obj.trigger_gravity(FLAG_HEIGHT_OFFSET - BLOCK_SIZE)
                obj.pass_through = True
            elif (obj.name == "block" and not obj.is_floor) or obj.name != "block":
                obj.trigger_gravity(HEIGHT*2)

        handle_move(player, objects)
        draw(window, background, bg_image, [player, *players], objects, offset_x)

    pygame.quit()
    quit()
