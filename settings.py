import pygame
import pygame_menu
import subprocess

pygame.init()

window = pygame.display.set_mode((800, 800))

menu = pygame_menu.Menu('Settings', 800, 800, theme=pygame_menu.themes.THEME_BLACK)




menu.mainloop(window)
