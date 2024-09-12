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
        Block((i * BLOCK_SIZE) - WIDTH, HEIGHT - BLOCK_SIZE, BLOCK_SIZE, True)
        for i in range(0, (WIDTH * 3) // BLOCK_SIZE)
    ]

    welcome_letters = [
        Text(8, TEXT_W),
        Text(8, TEXT_E),
        Text(8, TEXT_L),
        Text(8, TEXT_C),
        Text(8, TEXT_O),
        Text(8, TEXT_M),
        Text(8, TEXT_E),
        Text(8, TEXT_EXCLAMATION),
    ]
    # to figure out width do number of letters * scale * 7.8 then round
    welcome = Word(200, 100, 500, 80, welcome_letters)

    choose_letters = [
        Text(2, TEXT_C),
        Text(2, TEXT_H),
        Text(2, TEXT_O),
        Text(2, TEXT_O),
        Text(2, TEXT_S),
        Text(2, TEXT_E),
    ]
    choose = Word(275, 350, 95, 20, choose_letters)

    your_letters = [
        Text(2, TEXT_Y),
        Text(2, TEXT_O),
        Text(2, TEXT_U),
        Text(2, TEXT_R),
    ]
    your = Word(375, 350, 65, 20, your_letters)

    character_letters = [
        Text(2, TEXT_C),
        Text(2, TEXT_H),
        Text(2, TEXT_A),
        Text(2, TEXT_R),
        Text(2, TEXT_A),
        Text(2, TEXT_C),
        Text(2, TEXT_T),
        Text(2, TEXT_E),
        Text(2, TEXT_R),
        Text(2, TEXT_COLON),
    ]
    character = Word(450, 350, 155, 20, character_letters)

    words = [welcome, choose, your, character]

    player_options = [
        Player(
            (BLOCK_SIZE * 2.25) + (BLOCK_SIZE * 1.25 * i),
            PLAYER_OPTION_HEIGHT_OFFSET - BLOCK_SIZE,
            PLAYER_SIZE,
            PLAYER_OPTIONS[i],
        )
        for i in range(len(PLAYER_OPTIONS))
    ]

    objects = [*floor, *words]

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
