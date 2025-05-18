import pygame
from pygame.locals import *
import sys
import time
from styles import RED
from styles import BLACK
from styles import BLUE


def start_new_game(ch_lang):
    with open("saves.csv", "w") as file:
        file.write(f"0 1 {ch_lang}")
        file.close()



def no_saves_warning(window, window_width, window_height, fonts, ch_lang, languages):
    do_not_have_saves = fonts.font_size100.render(languages[ch_lang][6], 0, BLUE, BLACK)
    do_not_have_saves_place = ((window_width/2-window_width*0.3), window_height*0.4)
    window.blit(do_not_have_saves, do_not_have_saves_place)
    pygame.display.update()
    time.sleep(2)



def load_saved_state(choosen_lang, music):
    changed = False
    d1_saved = 0
    d2_saved = 0
    d3_saved = ""
    with open("saves.csv", "r") as file:
        row = file.readline().split(" ")
        d1 = int(row[0])
        d2 = int(row[1])
        d3 = str(row[2])
        if d3 != choosen_lang:
            changed = True
            d1_saved = d1
            d2_saved = d2
            d3_saved = choosen_lang
        file.close()
    
    if changed:
        with open("saves.csv", "w") as file:
            file.write(f"{str(d1_saved)} {str(d2_saved)} {d3_saved}")
            file.close()
        return d1_saved, d2_saved, d3_saved, music
    else:
        return d1, d2, d3, music




def menu_page(window_width, window_height, fonts, ch_lang, languages):

    window = pygame.display.set_mode((window_width, window_height))
    rects = [
        pygame.Rect(window_width*0.25, window_height*0.15, window_width*0.5, window_height*0.1),
        pygame.Rect(window_width*0.25, window_height*0.3, window_width*0.5, window_height*0.1),
        pygame.Rect(window_width*0.25, window_height*0.45, window_width*0.5, window_height*0.1),
        pygame.Rect(window_width*0.25, window_height*0.6, window_width*0.5, window_height*0.1),
        pygame.Rect(window_width*0.25, window_height*0.75, window_width*0.5, window_height*0.1)

    ]
    music_is_on = True
    run = 1
    while run:
        mouse = pygame.mouse.get_pos()
        
        window.fill((255, 255, 255))

        for rect in rects:
            square = pygame.draw.rect(window, BLACK, rect)
            if square.collidepoint(float(mouse[0]), float(mouse[1])):
                square = pygame.draw.rect(window, BLUE, rect)

        new_game_text = fonts.font_size50.render(languages[ch_lang][1], 0, RED)

        load_game_text = fonts.font_size50.render(languages[ch_lang][2], 0, RED)

        choosen_language_text = fonts.font_size50.render(languages[ch_lang][3], 0, RED)

        if music_is_on:
            music_button_text = fonts.font_size50.render(languages[ch_lang][4][0], 0, RED)
        else:
            music_button_text = fonts.font_size50.render(languages[ch_lang][4][1], 0, RED)

        quit_game_text = fonts.font_size50.render(languages[ch_lang][5], 0, RED)

        if ch_lang == "en":
            new_game_text_place = ((rects[0].center[0])-(rects[0].center[0]*0.17), rects[0].center[1]-15)

            load_game_text_place = ((rects[1].center[0])-(rects[1].center[0]*0.25), rects[1].center[1]-15)

            choosen_language_text_place = ((rects[2].center[0])-(rects[2].center[0]*0.4), rects[2].center[1]-15)

            music_button_text_place = ((rects[3].center[0])-(rects[3].center[0]*0.2), rects[3].center[1]-15)

            quit_game_text_place = ((rects[4].center[0])-(rects[4].center[0]*0.30), rects[4].center[1]-15)
            
        else:
            new_game_text_place = ((rects[0].center[0])-(rects[0].center[0]*0.13), rects[0].center[1]-15)

            load_game_text_place = ((rects[1].center[0])-(rects[1].center[0]*0.25), rects[1].center[1]-15)

            choosen_language_text_place = ((rects[2].center[0])-(rects[2].center[0]*0.35), rects[2].center[1]-15)

            music_button_text_place = ((rects[3].center[0])-(rects[3].center[0]*0.15), rects[3].center[1]-15)

            quit_game_text_place = ((rects[4].center[0])-(rects[4].center[0]*0.45), rects[4].center[1]-15)

        window.blit(new_game_text, new_game_text_place)
        window.blit(load_game_text, load_game_text_place)
        window.blit(choosen_language_text, choosen_language_text_place)
        window.blit(music_button_text, music_button_text_place)
        window.blit(quit_game_text, quit_game_text_place)


        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            elif event.type == pygame.MOUSEBUTTONDOWN:
                for rect in rects:
                    if rect.collidepoint(float(mouse[0]), float(mouse[1])):
                        if rects.index(rect) == 0:
                            try:
                                start_new_game(ch_lang)
                                data = load_saved_state(ch_lang, music_is_on)
                                run = 0
                                return data
                            except Exception as e:
                                no_saves_warning(window, window_width, window_height, fonts, ch_lang, languages)

                        elif rects.index(rect) == 1:
                            try:
                                data = load_saved_state(ch_lang, music_is_on)
                                return data
                            except Exception as e:
                                no_saves_warning(window, window_width, window_height, fonts, ch_lang, languages)

                        elif rects.index(rect) == 2:
                            if ch_lang == "en":
                                ch_lang = "hu"
                            else:
                                ch_lang = "en"
                        elif rects.index(rect) == 3:
                            if music_is_on:
                                music_is_on = False
                            else:
                                music_is_on = True

                        elif rects.index(rect) == len(rects)-1:
                            pygame.quit()
                            sys.exit()

        pygame.display.flip()