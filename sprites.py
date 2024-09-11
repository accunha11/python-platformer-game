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

class Player(pygame.sprite.Sprite): # sprites make it really easy to make pixel perfect collision, simplies collision code
    COLOR = (255, 0, 0) # class variable so it's the same for all players 
    GRAVITY = 1
    ANIMATION_DELAY = 3

    def __init__(self, x, y, width, height, sprites="NinjaFrog"):
        super().__init__()
        self.sprites = load_sprite_sheets("MainCharacters", sprites, 32, 32, True)
        self.rect = pygame.Rect(x, y, width, height)
        self.x_vel = 0
        self.y_vel = 0
        self.mask = None
        self.direction = "left" # need to know what direction the sprite is facing for animation purposes
        self.animation_count = 0 # resetting when changing directions
        self.fall_count = 0 # counts how long the player has been falling, used to increment gravity velocity
        self.jump_count = 0
        self.hit = False
        self.hit_count = 0
        self.score = 0

    def jump(self):
        self.y_vel = -self.GRAVITY * 8 # changing velocity going upwards and letting gravity bring it down
        self.animation_count = 0
        self.jump_count += 1
        if self.jump_count == 1: 
            self.fall_count = 0 # removing gravity so when we jump up again it's not taken into account

    def move(self, dx, dy):
        self.rect.x += dx
        self.rect.y += dy

    def make_hit(self):
        self.hit = True
        self.hit_count = 0
    
    def make_score(self):
        self.score += 1
    
    def move_left(self, vel):
        self.x_vel = -vel
        if self.direction != "left":
            self.direction = "left"
            self.animation_count = 0

    def move_right(self, vel):
        self.x_vel = vel
        if self.direction != "right":
            self.direction = "right"
            self.animation_count = 0
    
    def loop(self, fps): # be called once every frame, moves characters and updates animation
        self.y_vel += min(1, (self.fall_count / fps) * self.GRAVITY)
        self.move(self.x_vel, self.y_vel)

        if self.hit:
            self.hit_count += 1
        if self.hit_count > fps * 2:
            self.hit = False
            self.hit_count = 0

        self.fall_count += 1
        self.update_sprite()
    
    def landed(self):
        self.fall_count = 0
        self.y_vel = 0
        self.jump_count = 0
    
    def hit_head(self):
        self.count = 0
        self.y_vel *= -1

    def update_sprite(self):
        sprite_sheet = "idle"
        if self.hit:
            sprite_sheet = "hit"
        elif self.y_vel < 0:
            if self.jump_count == 1:
                sprite_sheet = "jump"
            elif self.jump_count == 2:
                sprite_sheet = "double_jump"
        elif self.y_vel > self.GRAVITY * 2: # make sure a significant gravity triggers the fall state
            sprite_sheet = "fall"
        elif self.x_vel != 0:
            sprite_sheet = "run"
        
        sprite_sheet_name = sprite_sheet + "_" + self.direction
        sprites = self.sprites[sprite_sheet_name]
        sprite_index = (self.animation_count // self.ANIMATION_DELAY) % len(sprites) # creates dynamic animations
        self.sprite = sprites[sprite_index]
        self.animation_count += 1
        self.update()

    def update(self):
        # makes sure the rectangle we use to bound is adjusted based on the sprite being used
        self.rect = self.sprite.get_rect(topleft=(self.rect.x, self.rect.y))
        self.mask = pygame.mask.from_surface(self.sprite)   # a mask is a mapping of all pixels that exist in the sprite
                                                            # this allows for pixel perfect collision instead of rectangles colliding
        
    def draw(self, win, offset_x):
        win.blit(self.sprite, (self.rect.x - offset_x, self.rect.y))

class Object(pygame.sprite.DirtySprite):
    def __init__(self, x, y, width, height, name=None):
        super().__init__()
        # All the properties we need for each sprite
        self.rect = pygame.Rect(x, y, width, height)
        self.image = pygame.Surface((width, height), pygame.SRCALPHA)
        self.width = width
        self.height = height
        self.name = name
    def draw(self, win, offset_x):
        win.blit(self.image, (self.rect.x - offset_x, self.rect.y))
class Block(Object):
    def __init__(self, x, y, size):
        super().__init__(x, y, size, size)
        block = get_block(size)
        self.image.blit(block, (0,0))
        self.mask = pygame.mask.from_surface(self.image)

class Fire(Object):
    ANIMATION_DELAY = 4

    def __init__(self, x, y, width, height):
        super().__init__(x, y, width, height, "fire")
        self.fire = load_sprite_sheets("Traps", "Fire", width, height)
        self.image = self.fire["off"][0]
        self.mask = pygame.mask.from_surface(self.image)
        self.animation_count = 0
        self.animation_name = "off"

    def on(self):
        self.animation_name = "on"
    
    def off(self):
        self.animation_name = "off"

    def loop(self):
        sprites = self.fire[self.animation_name]
        sprite_index = (self.animation_count // self.ANIMATION_DELAY) % len(sprites)
        self.image = sprites[sprite_index]
        self.animation_count += 1
        
        self.rect = self.image.get_rect(topleft=(self.rect.x, self.rect.y))
        self.mask = pygame.mask.from_surface(self.image)

        if self.animation_count // self.ANIMATION_DELAY > len(sprites):
            self.animation_count = 0 # letting the animation count get too big lags the program
class Box(Object):
    ANIMATION_DELAY = 3

    def __init__(self, x, y, width, height):
        super().__init__(x, y, width, height, "box")
        self.box = load_sprite_sheets("Items/Boxes", "Box2",
                                       width, height)
        self.image = self.box["Idle"][0]
        self.mask = pygame.mask.from_surface(self.image)
        self.animation_count = 0
        self.animation_name = "Idle"

    def make_hit(self):
        if self.animation_name == "Idle":
            self.animation_name = "Hit (28x24)"
    
    def loop(self):
        sprites = self.box[self.animation_name]
        sprite_index = (self.animation_count // self.ANIMATION_DELAY) % len(sprites)
        self.image = sprites[sprite_index]
        self.animation_count += 1
                    
        self.rect = self.image.get_rect(topleft=(self.rect.x, self.rect.y))
        self.mask = pygame.mask.from_surface(self.image)

        if sprite_index == (len(sprites) - 1):
            self.animation_count = 0
            if self.animation_name == "Hit (28x24)":
                self.animation_name = "Break"
            elif self.animation_name == "Break":
                self.rect = self.image.get_rect(topleft=(-1000, -1000))
                self.mask = pygame.mask.from_surface(self.image)


class Score(Object):

    def __init__(self, x, y, size, fruit_name):
        super().__init__(x, y, size, size, "score")
        self.score = load_sprite_sheets("Items", "Fruits",
                                       size, size)
        self.image = self.score[fruit_name][0]
        self.mask = pygame.mask.from_surface(self.image)

class Flag(Object):
    ANIMATION_DELAY = 3

    def __init__(self, x, y, size):
        super().__init__(x, y, size, size, "flag")
        self.flag = load_sprite_sheets("Items/Checkpoints", "Checkpoint",
                                       size, size)
        self.image = self.flag["Checkpoint (No Flag)"][0]
        self.mask = pygame.mask.from_surface(self.image)
        self.animation_count = 0
        self.animation_name = "Checkpoint (No Flag)"
        self.end_game = False

    def make_touch(self):
        if self.animation_name == "Checkpoint (No Flag)":
            self.animation_name = "Checkpoint (Flag Out) (64x64)"
            self.animation_count = 0
            self.end_game = True
    
    def loop(self):
        sprites = self.flag[self.animation_name]
        sprite_index = (self.animation_count // self.ANIMATION_DELAY) % len(sprites)
        self.image = sprites[sprite_index]
        self.animation_count += 1
                    
        self.rect = self.image.get_rect(topleft=(self.rect.x, self.rect.y))
        self.mask = pygame.mask.from_surface(self.image)

        if sprite_index == (len(sprites) - 1):
            self.animation_count = 0
            if self.animation_name == "Checkpoint (Flag Out) (64x64)":
                self.animation_name = "Checkpoint (Flag Idle)(64x64)"

class Fruit(Object):
    ANIMATION_DELAY = 3

    def __init__(self, x, y, size, fruit_name, visible=True):
        super().__init__(x, y, size, size, "fruit")
        self.fruit = load_sprite_sheets("Items", "Fruits",
                                       size, size)
        if visible:
            self.image = self.fruit[fruit_name][0]
            self.mask = pygame.mask.from_surface(self.image)
        self.animation_count = 0
        self.fruit_name = fruit_name
        self.animation_name = fruit_name
        self.collected = False
        self.visible = visible
    
    def change_visibility(self):
        self.visible = not self.visible

    def make_touch(self, player):
        if self.animation_name == self.fruit_name:
            self.animation_name = "Collected"
            self.animation_count = 0
            player.make_score()

    def loop(self):
        if self.visible and not self.collected:
            sprites = self.fruit[self.animation_name]
            sprite_index = (self.animation_count // self.ANIMATION_DELAY) % len(sprites)
            self.image = sprites[sprite_index]
            self.animation_count += 1
                            
            self.rect = self.image.get_rect(topleft=(self.rect.x, self.rect.y))
            self.mask = pygame.mask.from_surface(self.image)

            if sprite_index == (len(sprites) - 1):
                self.animation_count = 0
                if self.animation_name == "Collected":
                    if not self.collected:
                        self.collected = True
                        self.visible = False
                        self.rect = self.image.get_rect(topleft=(-1000, -1000))
                        self.mask = pygame.mask.from_surface(self.image)
