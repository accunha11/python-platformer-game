import pygame
from helpers.constants import *

from helpers.helper_functions import get_background, draw, handle_move
from levels.level1 import level1


def transition(window, player, objects, players):
    clock = pygame.time.Clock()
    background, bg_image = get_background("Blue.png")

    offset_x = 0
    scroll_area_width = BLOCK_SIZE

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

        if player.rect.right >= WIDTH + BLOCK_SIZE * 2:
            player.rect.right = BLOCK_SIZE * 2
            level1(window, player)
            break

        for pl in players:
            if pl.rect.y < 2*HEIGHT:
                pl.loop()
                pl.pass_through = True
                handle_move(player, objects)

        for obj in objects:
            if (obj.name == "block" and not obj.is_floor) or obj.name != "block":
                obj.trigger_gravity(HEIGHT*2)

        handle_move(player, objects)
        draw(window, background, bg_image, [player, *players], objects, offset_x)

        if (
            (player.rect.right - offset_x >= WIDTH - scroll_area_width * 2)
            and (player.x_vel > 0)
        ) or (
            (player.rect.left - offset_x <= scroll_area_width)
            and (player.x_vel < 0)
            and (player.rect.left > scroll_area_width)
        ):
            offset_x += player.x_vel

    pygame.quit()
    quit()
