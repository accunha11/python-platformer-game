import pygame
from helpers.constants import *

pygame.init()
pygame.display.set_caption("Platformer")
window = pygame.display.set_mode((WIDTH, HEIGHT))

from sprites.objects import *
from sprites.player import *
from helpers.helper_functions import *
from screens.transition import transition


def main(window):
    clock = pygame.time.Clock()
    background, bg_image = get_background("Blue.png")

    floor = [
        Block(i * BLOCK_SIZE, HEIGHT - BLOCK_SIZE, BLOCK_SIZE, True)
        for i in range(0, (WIDTH * 2) // BLOCK_SIZE)
    ]

    letter = Text(100, 100, 4, TEXT_A)

    player_options = [
        Player(
            (BLOCK_SIZE * 2.25) + (BLOCK_SIZE * 1.25 * i),
            PLAYER_OPTION_HEIGHT_OFFSET - BLOCK_SIZE*3,
            PLAYER_SIZE,
            PLAYER_OPTIONS[i],
        )
        for i in range(len(PLAYER_OPTIONS))
    ]

    objects = [*floor, letter]

    run = True
    while run:
        clock.tick(FPS)  # regulate frame rate across different devices

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break

            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    click_pos = pygame.mouse.get_pos()
                    for player in player_options:
                        if player.clicked(click_pos):
                            player_options.remove(player)
                            transition(window, player, objects, player_options)
                            break

        for player in player_options:
            player.loop()
            handle_move(player, objects, True)

        draw(window, background, bg_image, player_options, objects)

    pygame.quit()
    quit()


if __name__ == "__main__":
    main(window)
