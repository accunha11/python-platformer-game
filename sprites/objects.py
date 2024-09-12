import pygame

from .sprite_helpers import *
from helpers.constants import *


class Object(pygame.sprite.DirtySprite):
    GRAVITY = 20

    def __init__(self, x, y, width, height, name=None, pass_through=False):
        super().__init__()
        # All the properties we need for each sprite
        self.rect = pygame.Rect(x, y, width, height)
        self.image = pygame.Surface((width, height), pygame.SRCALPHA)
        self.mask = pygame.mask.from_surface(self.image)
        self.width = width
        self.height = height
        self.name = name
        self.pass_through = pass_through
        self.x = x
        self.y = y
        self.fall_count = 0

    def clicked(self, position):
        x, y = position
        x -= self.rect.x
        y -= self.rect.y
        try:
            self.mask.get_at((x, y))
            return True
        except IndexError:
            return False

    def trigger_gravity(self, stop=HEIGHT):
        self.pass_through = True
        if self.rect.y < stop:
            self.rect.y += (self.fall_count / FPS) * self.GRAVITY
            self.fall_count += 1
        else:
            self.land()

    def land(self):
        self.pass_through = False

    def draw(self, win, offset_x):
        win.blit(self.image, (self.rect.x - offset_x, self.rect.y))


class Word(Object):

    def __init__(self, x, y, width, height, text=[]):
        super().__init__(x, y, width, height)
        for i in range(len(text)):
            self.image.blit(text[i].image, ((width // len(text)) * i, 0))
        self.mask = pygame.mask.from_surface(self.image)


class Text(Object):

    def __init__(self, scale, letter_tuple, x=0, y=0, is_white=True):
        super().__init__(x, y, width=8 * scale, height=10 * scale)
        text = get_text(letter_tuple, scale, is_white)
        self.image.blit(text, (0, 0))
        self.mask = pygame.mask.from_surface(self.image)


class Block(Object):

    def __init__(self, x, y, size, is_floor=False):
        super().__init__(x, y, size, size, "block")
        block = get_block(size)
        self.image.blit(block, (0, 0))
        self.mask = pygame.mask.from_surface(self.image)
        self.is_floor = is_floor


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
            self.animation_count = (
                0  # letting the animation count get too big lags the program
            )


class Box(Object):
    ANIMATION_DELAY = 3

    def __init__(self, x, y, width, height):
        super().__init__(x, y, width, height, "box")
        self.box = load_sprite_sheets("Items/Boxes", "Box2", width, height)
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
        self.score = load_sprite_sheets("Items", "Fruits", size, size)
        self.image = self.score[fruit_name][0]
        self.mask = pygame.mask.from_surface(self.image)


class Start_Flag(Object):
    ANIMATION_DELAY = 3

    def __init__(self, x, y, size):
        super().__init__(x, y, size, size, "start_flag")
        self.flag = load_sprite_sheets("Items/Checkpoints", "Start", size, size)
        self.image = self.flag["Start (Moving) (64x64)"][0]
        self.mask = pygame.mask.from_surface(self.image)
        self.animation_count = 0
        self.animation_name = "Start (Moving) (64x64)"
        self.pass_through = True

    def loop(self):
        sprites = self.flag[self.animation_name]
        sprite_index = (self.animation_count // self.ANIMATION_DELAY) % len(sprites)
        self.image = sprites[sprite_index]
        self.animation_count += 1

        self.rect = self.image.get_rect(topleft=(self.rect.x, self.rect.y))
        self.mask = pygame.mask.from_surface(self.image)

        if self.animation_count // self.ANIMATION_DELAY > len(sprites):
            self.animation_count = (
                0  # letting the animation count get too big lags the program
            )


class Flag(Object):
    ANIMATION_DELAY = 3

    def __init__(self, x, y, size):
        super().__init__(x, y, size, size, "flag")
        self.flag = load_sprite_sheets("Items/Checkpoints", "Checkpoint", size, size)
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
        super().__init__(x, y, size, size, "fruit", True)
        self.fruit = load_sprite_sheets("Items", "Fruits", size, size)
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
