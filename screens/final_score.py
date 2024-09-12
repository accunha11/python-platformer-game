import pygame
from helpers.constants import *

from sprites.objects import *
from sprites.player import *
from helpers.helper_functions import *


def final_score(window, score):
    clock = pygame.time.Clock()
    background, bg_image = get_background("Blue.png")

    congrats_letters = [
        Text(8, TEXT_C),
        Text(8, TEXT_O),
        Text(8, TEXT_N),
        Text(8, TEXT_G),
        Text(8, TEXT_R),
        Text(8, TEXT_A),
        Text(8, TEXT_T),
        Text(8, TEXT_S),
        Text(8, TEXT_EXCLAMATION),
    ]
    congrats = Word(160, 100, 560, 80, congrats_letters)

    better_letters = [
        Text(6, TEXT_B),
        Text(6, TEXT_E),
        Text(6, TEXT_T),
        Text(6, TEXT_T),
        Text(6, TEXT_E),
        Text(6, TEXT_R),
    ]
    better = Word(180, 100, 280, 60, better_letters)

    luck_letters = [
        Text(6, TEXT_L),
        Text(6, TEXT_U),
        Text(6, TEXT_C),
        Text(6, TEXT_K),
    ]
    luck = Word(495, 100, 190, 60, luck_letters)

    next_letters = [
        Text(6, TEXT_N),
        Text(6, TEXT_E),
        Text(6, TEXT_X),
        Text(6, TEXT_T),
    ]
    next = Word(210, 170, 190, 60, next_letters)

    time_letters = [
        Text(6, TEXT_T),
        Text(6, TEXT_I),
        Text(6, TEXT_M),
        Text(6, TEXT_E),
        Text(6, TEXT_EXCLAMATION),
    ]
    time = Word(430, 170, 235, 60, time_letters)

    your_letters = [
        Text(3, TEXT_Y),
        Text(3, TEXT_O),
        Text(3, TEXT_U),
        Text(3, TEXT_R),
    ]
    your = Word(280, 275, 95, 30, your_letters)

    score_letters = [
        Text(3, TEXT_S),
        Text(3, TEXT_C),
        Text(3, TEXT_O),
        Text(3, TEXT_R),
        Text(3, TEXT_E),
    ]
    score_word = Word(390, 275, 117, 30, score_letters)

    letters_is = [
        Text(3, TEXT_I),
        Text(3, TEXT_S),
        Text(3, TEXT_COLON),
    ]
    word_is = Word(520, 275, 70, 30, letters_is)

    of_letters = [
        Text(3, TEXT_O),
        Text(3, TEXT_F)
    ]
    of_word = Word(410, 320, 47, 30, of_letters)

    number_5 = [
        Text(3, TEXT_5)
    ]
    word_5_max = Word(460, 320, 25, 30, number_5)
    word_5_score = Word(380, 320, 25, 30, number_5)

    number_4 = [Text(3, TEXT_4)]
    word_4_score = Word(380, 320, 25, 30, number_4)

    number_3 = [Text(3, TEXT_3)]
    word_3_score = Word(380, 320, 25, 30, number_3)

    number_2 = [Text(3, TEXT_2)]
    word_2_score = Word(380, 320, 25, 30, number_2)

    number_1 = [Text(3, TEXT_1)]
    word_1_score = Word(380, 320, 25, 30, number_1)

    generic_words = [your, score_word, word_is, of_word, word_5_max]

    objects = [*generic_words]

    trophy = Trophy(370, 400, 64)

    if score >= 4:
        objects.append(congrats)
        if score == 5:
            objects.append(word_5_score)
            objects.append(trophy)
        elif score == 4:
            objects.append(word_4_score)
    else:
        objects.append(better)
        objects.append(luck)
        objects.append(next)
        objects.append(time)
        if score == 3:
            objects.append(word_3_score)
        elif score == 2:
            objects.append(word_2_score)
        elif score == 1:
            objects.append(word_1_score)

    offset_x = WIDTH

    run = True
    while run:
        clock.tick(FPS)  # regulate frame rate across different devices

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break

        if offset_x > 0:
            offset_x -= 5
        
        trophy.loop()

        draw(window, background, bg_image, [], objects, offset_x)

    pygame.quit()
    quit()
