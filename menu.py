import pygame
from pygame.locals import *
import sys

def menu_page(window_width, window_height, fonts, resolutions):
    index = -1
    for i in range(len(resolutions)):
        if resolutions[i][0] == window_width and resolutions[i][1] == window_height:
            index = i
    action = 0
    window = pygame.display.set_mode((window_width, window_height), pygame.FULLSCREEN|pygame.SCALED)
    rects = [pygame.Rect(window_width*0.38, window_height*0.25, window_width*0.25, window_height*0.1), pygame.Rect(window_width*0.38, window_height/2, window_width*0.25, window_height*0.1)]
    run = 1
    while run:
        mouse = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                for rect in rects:
                    if rect.collidepoint(float(mouse[0]), float(mouse[1])):
                        if rects.index(rect) == 0:
                            action = 1
                            run = 0
                            return action
                        elif rects.index(rect) == 1:
                            pygame.quit()
                            sys.exit()


        
        window.fill((255, 255, 255))

        for rect in rects:
            square = pygame.draw.rect(window, (0, 0, 0), rect)
            if square.collidepoint(float(mouse[0]), float(mouse[1])):
                square = pygame.draw.rect(window, (0, 0, 255), rect)

        new_game_text = fonts["50"].render("New game", 0, (255, 0, 0))
        
        if index == 14:
            new_game_text_place = ((rects[0].center[0])-(rects[0].center[0]*0.15+18), rects[0].center[1]-15)
        else:
            new_game_text_place = ((rects[0].center[0])-(rects[0].center[0]*0.15-40), rects[0].center[1]-15)

        quit_game_text = fonts["50"].render("Quit game", 0, (255, 0, 0))
        if index == 14: 
            quit_game_text_place = ((rects[1].center[0])-(rects[1].center[0]*0.15+18), rects[1].center[1]-15)
        else:
            quit_game_text_place = ((rects[1].center[0])-(rects[1].center[0]*0.15-40.5), rects[1].center[1]-15)
        window.blit(new_game_text, new_game_text_place)
        window.blit(quit_game_text, quit_game_text_place)



        pygame.display.flip()