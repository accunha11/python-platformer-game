import pygame
from os import listdir
from os.path import isfile, join

def flip(sprites):
    return [pygame.transform.flip(sprite, True, False) for sprite in sprites]

def load_sprite_sheets(dir1, dir2, width, height, direction=False):
    path = join("assets", dir1, dir2)
    images = [f for f in listdir(path) if isfile(join(path, f))] # load every single file that is inside a character's directory

    all_sprites = {} # key is animation style and value is images in animation

    for image in images:
        sprite_sheet = pygame.image.load(join(path, image)).convert_alpha() # convert alpha gives transparent background

        sprites = []
        for i in range(sprite_sheet.get_width() // width):
            # Need to create a surface that is the desired size of the animation frame
            # Then, we need to grab the animation frame from the main image
            # We need to draw that onto the surface and then export the surface
            surface = pygame.Surface((width, height), pygame.SRCALPHA, 32)
            rect = pygame.Rect(i * width, 0, width, height)
            surface.blit(sprite_sheet, (0,0), rect) # source, destination, area of the source that we're drawing
            sprites.append(pygame.transform.scale2x(surface))
        
        if direction:
            all_sprites[image.replace(".png", "") + "_right"] = sprites
            all_sprites[image.replace(".png", "") + "_left"] = flip(sprites)
        else:
            all_sprites[image.replace(".png", "")] = sprites

    return all_sprites

def get_block(size):
    path = join("assets", "Terrain", "Terrain.png")
    image = pygame.image.load(path).convert_alpha()
    surface = pygame.Surface((size, size), pygame.SRCALPHA, 32)
    rect = pygame.Rect(96, 0, size, size) #change number values and size to load a different image for our block
    surface.blit(image, (0, 0), rect)
    return pygame.transform.scale2x(surface)