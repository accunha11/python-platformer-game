import pygame

from .sprite_helpers import load_sprite_sheets


class Player(
    pygame.sprite.Sprite
):  # sprites make it really easy to make pixel perfect collision, simplies collision code
    COLOR = (255, 0, 0)  # class variable so it's the same for all players
    GRAVITY = 1
    ANIMATION_DELAY = 3

    def __init__(self, x, y, width, height, sprites="NinjaFrog"):
        super().__init__()
        self.sprites = load_sprite_sheets("MainCharacters", sprites, 32, 32, True)
        self.rect = pygame.Rect(x, y, width, height)
        self.x_vel = 0
        self.y_vel = 0
        self.mask = None
        self.direction = "left"  # need to know what direction the sprite is facing for animation purposes
        self.animation_count = 0  # resetting when changing directions
        self.fall_count = 0  # counts how long the player has been falling, used to increment gravity velocity
        self.jump_count = 0
        self.hit = False
        self.hit_count = 0
        self.score = 0

    def jump(self):
        self.y_vel = (
            -self.GRAVITY * 8
        )  # changing velocity going upwards and letting gravity bring it down
        self.animation_count = 0
        self.jump_count += 1
        if self.jump_count == 1:
            self.fall_count = 0  # removing gravity so when we jump up again it's not taken into account

    def move(self, dx, dy):
        self.rect.x += dx
        self.rect.y += dy

    def make_hit(self):
        self.hit = True
        self.hit_count = 0

    def make_score(self):
        self.score += 1

    def clicked(self, position):
        x, y = position
        x -= self.rect.x
        y -= self.rect.y
        try:
            self.mask.get_at((x, y))
            return True
        except IndexError:
            return False

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

    def loop(
        self, fps
    ):  # be called once every frame, moves characters and updates animation
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
        elif (
            self.y_vel > self.GRAVITY * 2
        ):  # make sure a significant gravity triggers the fall state
            sprite_sheet = "fall"
        elif self.x_vel != 0:
            sprite_sheet = "run"

        sprite_sheet_name = sprite_sheet + "_" + self.direction
        sprites = self.sprites[sprite_sheet_name]
        sprite_index = (self.animation_count // self.ANIMATION_DELAY) % len(
            sprites
        )  # creates dynamic animations
        self.sprite = sprites[sprite_index]
        self.animation_count += 1
        self.update()

    def update(self):
        # makes sure the rectangle we use to bound is adjusted based on the sprite being used
        self.rect = self.sprite.get_rect(topleft=(self.rect.x, self.rect.y))
        self.mask = pygame.mask.from_surface(
            self.sprite
        )  # a mask is a mapping of all pixels that exist in the sprite
        # this allows for pixel perfect collision instead of rectangles colliding

    def draw(self, win, offset_x):
        win.blit(self.sprite, (self.rect.x - offset_x, self.rect.y))
