import pygame
from os.path import join

WIDTH, HEIGHT = 875, 700
FPS = 60
PLAYER_VEL = 5

def get_background(name):
    # the code MUST be run from the directory that the code lives in
    image = pygame.image.load(join("assets", "Background", name))
    _, _, width, height = image.get_rect() # underscores are there because I don't need the other two values
    tiles = []

    for i in range(WIDTH // width + 1):
        for j in range(HEIGHT // height + 1):
            pos = (i * width, j * height)   # denotes the position of the top left hand corner of the current tile
                                            # when you draw something on the screen in pygame, you draw it from the top
                                            # left hand corner. This continuously move positions.
            tiles.append(pos)
    
    return tiles, image

def draw(window, background, bg_image, player, objects, offset_x=0, scoring=[]):
    for tile in background: # looping through every tile we have and drawing background image at that posiiton
        window.blit(bg_image, tile)
    
    for score in scoring:
        score.draw(window, 0)
    
    for obj in objects:
        obj.draw(window, offset_x)

    player.draw(window, offset_x)

    pygame.display.update()

def handle_vertical_collision(player, objects, dy):
    collided_objects = []
    for obj in objects:
        if pygame.sprite.collide_mask(player, obj):
            if obj.name != "fruit":
                
                if dy > 0:
                    player.rect.bottom = obj.rect.top
                    player.landed()
                elif dy < 0:
                    player.rect.top = obj.rect.bottom # makes sure we don't go through the objects
                    player.hit_head()
                    if obj.name == "box":
                        obj.make_hit()

                collided_objects.append(obj)
            else:
                obj.make_touch(player)
    
    return collided_objects

def collide(player, objects, dx):
    player.move(dx, 0) # move the player preemptively to check if it will hit a block
    player.update()
    collided_object = None

    for obj in objects:
        if pygame.sprite.collide_mask(player, obj):
            if obj.name == "fruit":
                obj.make_touch(player)
                break
            else:
                collided_object = obj
                break

    player.move(-dx, 0)
    player.update()

    return collided_object

def handle_move(player, objects, game_over=False):
    keys = pygame.key.get_pressed()

    player.x_vel = 0 # resetting velocity
    collide_left = collide(player, objects, -PLAYER_VEL * 2) # multiplies by 2 so there's space between the blocks so we don't get sprite glitches
    collide_right = collide(player, objects, PLAYER_VEL * 2)

    if keys[pygame.K_LEFT] and not collide_left and not game_over:
        player.move_left(PLAYER_VEL)
    if keys[pygame.K_RIGHT] and not collide_right and not game_over:
        player.move_right(PLAYER_VEL)
    
    vertical_collide = handle_vertical_collision(player, objects, player.y_vel)
    to_check = [collide_left, collide_right, *vertical_collide]
    for obj in to_check:
        if obj and obj.name == "fire":
            player.make_hit()
        if obj and obj.name == "flag":
            obj.make_touch()