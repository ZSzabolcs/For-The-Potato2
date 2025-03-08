import pygame
from pygame.locals import *
import sys
import time
from styles import RED
from styles import BLACK
from styles import BLUE


def start_new_game():
    with open("saves.csv", "w") as file:
        file.write("0 1")
        file.close()



def no_saves_warning(window, window_width, window_height, fonts):
    do_not_have_saves = fonts.font_size100.render("You don't have saves!", 0, BLUE, BLACK)
    do_not_have_saves_place = ((window_width/2-window_width*0.3), window_height*0.4)
    window.blit(do_not_have_saves, do_not_have_saves_place)
    pygame.display.update()
    time.sleep(2)



def load_saved_state():
    with open("saves.csv", "r") as file:
        row = file.readline().split(" ")
        d1 = int(row[0])
        d2 = int(row[1])
        file.close()
        return d1, d2




def menu_page(window_width, window_height, fonts):

    window = pygame.display.set_mode((window_width, window_height))
    rects = [
        pygame.Rect(window_width*0.38, window_height*0.15, window_width*0.25, window_height*0.1),
        pygame.Rect(window_width*0.38, window_height*0.3, window_width*0.25, window_height*0.1),
        pygame.Rect(window_width*0.25, window_height*0.45, window_width*0.5, window_height*0.1),
        pygame.Rect(window_width*0.38, window_height*0.6, window_width*0.25, window_height*0.1)
    ]
    run = 1
    while run:
        mouse = pygame.mouse.get_pos()
        
        window.fill((255, 255, 255))

        for rect in rects:
            square = pygame.draw.rect(window, BLACK, rect)
            if square.collidepoint(float(mouse[0]), float(mouse[1])):
                square = pygame.draw.rect(window, BLUE, rect)

        new_game_text = fonts.font_size50.render("New game", 0, RED)
        new_game_text_place = ((rects[0].center[0])-(rects[0].center[0]*0.17), rects[0].center[1]-15)

        load_game_text = fonts.font_size50.render("Load game", 0, RED)
        load_game_text_place = ((rects[1].center[0])-(rects[1].center[0]*0.17), rects[1].center[1]-15)

        choosen_language_text = fonts.font_size50.render("Game language: English", 0, RED)
        choosen_language_text_place = ((rects[2].center[0])-(rects[2].center[0]*0.4), rects[2].center[1]-15)

        quit_game_text = fonts.font_size50.render("Quit game", 0, RED)
        quit_game_text_place = ((rects[3].center[0])-(rects[3].center[0]*0.17), rects[3].center[1]-15)

        window.blit(new_game_text, new_game_text_place)
        window.blit(load_game_text, load_game_text_place)
        window.blit(choosen_language_text, choosen_language_text_place)
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
                                start_new_game()
                                d1, d2 = load_saved_state()
                                run = 0
                                return d1, d2
                            except Exception as e:
                                no_saves_warning(window, window_width, window_height, fonts)

                        elif rects.index(rect) == 1:
                            try:
                                d1, d2 = load_saved_state()
                                return d1, d2
                            except Exception as e:
                                no_saves_warning(window, window_width, window_height, fonts)

                        elif rects.index(rect) == 2:
                            action = 3
                        elif rects.index(rect) == 3:
                            pygame.quit()
                            sys.exit()

        pygame.display.flip()