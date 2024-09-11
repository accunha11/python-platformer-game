import pygame
import constants

from sprites import Block, Box, Player, Flag, Fire, Fruit, Score
from helper_functions import get_background, draw, handle_move

def level1(window):
    clock = pygame.time.Clock()
    background, bg_image = get_background("Blue.png")

    player = Player(100, 100, 50, 50)
    fire = Fire(constants.BLOCK_SIZE*6.35, constants.FIRE_HEIGHT_OFFSET - constants.BLOCK_SIZE + (constants.BLOCK_SIZE * 2) // 3, 16, 32)
    fire.on()

    box = Box(constants.BLOCK_SIZE*6.25, constants.HEIGHT - constants.BLOCK_SIZE * 2.85, constants.BOX_WIDTH, constants.BOX_HEIGHT)
    hidden_fruit = Fruit(constants.BLOCK_SIZE*6.25 + constants.HIDDEN_FRUIT_WIDTH_OFFSET, constants.HIDDEN_FRUIT_HEIGHT_OFFSET - constants.BLOCK_SIZE * 2.85, constants.FRUIT_SIZE, "Strawberry", False)

    flag = Flag(constants.BLOCK_SIZE*20, constants.FLAG_HEIGHT_OFFSET - constants.BLOCK_SIZE * 5, constants.FLAG_SIZE)
    fruits = [Fruit(constants.BLOCK_SIZE* 9 + 15, constants.FRUIT_HEIGHT_OFFSET - constants.BLOCK_SIZE * 4, constants.FRUIT_SIZE, "Strawberry"),
              Fruit(constants.BLOCK_SIZE* 10 + 15, constants.FRUIT_HEIGHT_OFFSET - constants.BLOCK_SIZE * 4, constants.FRUIT_SIZE, "Strawberry"),
              Fruit(constants.BLOCK_SIZE* 15 + 15, constants.FRUIT_HEIGHT_OFFSET - constants.BLOCK_SIZE * 4, constants.FRUIT_SIZE, "Strawberry"),
              Fruit(constants.BLOCK_SIZE* 16 + 15, constants.FRUIT_HEIGHT_OFFSET - constants.BLOCK_SIZE * 4, constants.FRUIT_SIZE, "Strawberry"),]

    floor = [Block(i * constants.BLOCK_SIZE, constants.HEIGHT - constants.BLOCK_SIZE, constants.BLOCK_SIZE) 
             for i in range(0, (constants.WIDTH * 2) // constants.BLOCK_SIZE)]
    
    floor[6] = Block(constants.BLOCK_SIZE * 6, constants.HEIGHT - constants.BLOCK_SIZE // 3, constants.BLOCK_SIZE)

    begin_wall = [Block(0, constants.HEIGHT - constants.BLOCK_SIZE * i, constants.BLOCK_SIZE) for i in range(0,9)]

    extra_blocks = [Block(constants.BLOCK_SIZE * 9, constants.HEIGHT - constants.BLOCK_SIZE * 4, constants.BLOCK_SIZE),
                    Block(constants.BLOCK_SIZE * 10, constants.HEIGHT - constants.BLOCK_SIZE * 4, constants.BLOCK_SIZE),
                    Block(constants.BLOCK_SIZE * 12, constants.HEIGHT - constants.BLOCK_SIZE * 3, constants.BLOCK_SIZE),
                    Block(constants.BLOCK_SIZE * 13, constants.HEIGHT - constants.BLOCK_SIZE * 3, constants.BLOCK_SIZE),
                    Block(constants.BLOCK_SIZE * 15, constants.HEIGHT - constants.BLOCK_SIZE * 4, constants.BLOCK_SIZE),
                    Block(constants.BLOCK_SIZE * 16, constants.HEIGHT - constants.BLOCK_SIZE * 4, constants.BLOCK_SIZE)]
    
    ending_blocks = [Block(constants.BLOCK_SIZE * 19, constants.HEIGHT - constants.BLOCK_SIZE * 5, constants.BLOCK_SIZE),
                     Block(constants.BLOCK_SIZE * 20, constants.HEIGHT - constants.BLOCK_SIZE * 5, constants.BLOCK_SIZE)]
    
    objects = [*floor, *begin_wall, *extra_blocks, *ending_blocks, fire, flag, box, *fruits, hidden_fruit]

    offset_x = 0
    scroll_area_width = constants.BLOCK_SIZE

    run = True
    while run:
        clock.tick(constants.FPS) #regulate frame rate across different devices

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break
                
            if event.type == pygame.KEYDOWN and not flag.end_game:
                if event.key == pygame.K_SPACE and player.jump_count < 2:
                    player.jump()
        
        player.loop(constants.FPS)
        fire.loop()
        flag.loop()
        box.loop()

        if box.animation_name == "Break":
            hidden_fruit.change_visibility()

        hidden_fruit.loop()

        for fruit in fruits:
            fruit.loop()

        scoring = [Score(constants.WIDTH - constants.FRUIT_SIZE * i - 75, 25, constants.FRUIT_SIZE, "Strawberry") for i in range(player.score)]

        handle_move(player, objects, flag.end_game)
        draw(window, background, bg_image, player, objects, offset_x, scoring)

        if((player.rect.right - offset_x >= constants.WIDTH - scroll_area_width * 2) and (player.x_vel > 0)) or (
                (player.rect.left - offset_x <= scroll_area_width) and (player.x_vel < 0) and 
                (player.rect.left - offset_x + scroll_area_width > 0)):
            offset_x += player.x_vel
    
    pygame.quit()
    quit()