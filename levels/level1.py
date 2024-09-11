import pygame
from helpers.constants import *

from sprites.objects import Block, Box, Flag, Fire, Fruit, Score
from sprites.player import Player
from helpers.helper_functions import get_background, draw, handle_move


def level1(window):
    clock = pygame.time.Clock()
    background, bg_image = get_background("Blue.png")

    player = Player(100, 100, 50, 50)
    fire = Fire(
        BLOCK_SIZE * 6.35,
        FIRE_HEIGHT_OFFSET - BLOCK_SIZE + (BLOCK_SIZE * 2) // 3,
        16,
        32,
    )
    fire.on()

    box = Box(BLOCK_SIZE * 6.25, HEIGHT - BLOCK_SIZE * 2.85, BOX_WIDTH, BOX_HEIGHT)
    hidden_fruit = Fruit(
        BLOCK_SIZE * 6.25 + HIDDEN_FRUIT_WIDTH_OFFSET,
        HIDDEN_FRUIT_HEIGHT_OFFSET - BLOCK_SIZE * 2.85,
        FRUIT_SIZE,
        "Strawberry",
        False,
    )

    flag = Flag(BLOCK_SIZE * 20, FLAG_HEIGHT_OFFSET - BLOCK_SIZE * 5, FLAG_SIZE)
    fruits = [
        Fruit(
            BLOCK_SIZE * 9 + 15,
            FRUIT_HEIGHT_OFFSET - BLOCK_SIZE * 4,
            FRUIT_SIZE,
            "Strawberry",
        ),
        Fruit(
            BLOCK_SIZE * 10 + 15,
            FRUIT_HEIGHT_OFFSET - BLOCK_SIZE * 4,
            FRUIT_SIZE,
            "Strawberry",
        ),
        Fruit(
            BLOCK_SIZE * 15 + 15,
            FRUIT_HEIGHT_OFFSET - BLOCK_SIZE * 4,
            FRUIT_SIZE,
            "Strawberry",
        ),
        Fruit(
            BLOCK_SIZE * 16 + 15,
            FRUIT_HEIGHT_OFFSET - BLOCK_SIZE * 4,
            FRUIT_SIZE,
            "Strawberry",
        ),
    ]

    floor = [
        Block(i * BLOCK_SIZE, HEIGHT - BLOCK_SIZE, BLOCK_SIZE)
        for i in range(0, (WIDTH * 2) // BLOCK_SIZE)
    ]

    floor[6] = Block(BLOCK_SIZE * 6, HEIGHT - BLOCK_SIZE // 3, BLOCK_SIZE)

    begin_wall = [Block(0, HEIGHT - BLOCK_SIZE * i, BLOCK_SIZE) for i in range(0, 9)]

    extra_blocks = [
        Block(BLOCK_SIZE * 9, HEIGHT - BLOCK_SIZE * 4, BLOCK_SIZE),
        Block(BLOCK_SIZE * 10, HEIGHT - BLOCK_SIZE * 4, BLOCK_SIZE),
        Block(BLOCK_SIZE * 12, HEIGHT - BLOCK_SIZE * 3, BLOCK_SIZE),
        Block(BLOCK_SIZE * 13, HEIGHT - BLOCK_SIZE * 3, BLOCK_SIZE),
        Block(BLOCK_SIZE * 15, HEIGHT - BLOCK_SIZE * 4, BLOCK_SIZE),
        Block(BLOCK_SIZE * 16, HEIGHT - BLOCK_SIZE * 4, BLOCK_SIZE),
    ]

    ending_blocks = [
        Block(BLOCK_SIZE * 19, HEIGHT - BLOCK_SIZE * 5, BLOCK_SIZE),
        Block(BLOCK_SIZE * 20, HEIGHT - BLOCK_SIZE * 5, BLOCK_SIZE),
    ]

    objects = [
        *floor,
        *begin_wall,
        *extra_blocks,
        *ending_blocks,
        fire,
        flag,
        box,
        *fruits,
        hidden_fruit,
    ]

    offset_x = 0
    scroll_area_width = BLOCK_SIZE

    run = True
    while run:
        clock.tick(FPS)  # regulate frame rate across different devices

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break

            if event.type == pygame.KEYDOWN and not flag.end_game:
                if event.key == pygame.K_SPACE and player.jump_count < 2:
                    player.jump()

        player.loop(FPS)
        fire.loop()
        flag.loop()
        box.loop()

        if box.animation_name == "Break":
            hidden_fruit.change_visibility()

        hidden_fruit.loop()

        for fruit in fruits:
            fruit.loop()

        scoring = [
            Score(WIDTH - FRUIT_SIZE * i - 75, 25, FRUIT_SIZE, "Strawberry")
            for i in range(player.score)
        ]

        handle_move(player, objects, flag.end_game)
        draw(window, background, bg_image, player, objects, offset_x, scoring)

        if (
            (player.rect.right - offset_x >= WIDTH - scroll_area_width * 2)
            and (player.x_vel > 0)
        ) or (
            (player.rect.left - offset_x <= scroll_area_width)
            and (player.x_vel < 0)
            and (player.rect.left - offset_x + scroll_area_width > 0)
        ):
            offset_x += player.x_vel

    pygame.quit()
    quit()
