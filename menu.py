import pygame
from pygame.locals import *
import os
import worlds
import sys

run = 1
while run:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			
			pygame.quit()
			sys.exit()
	
	square1 = pygame.draw.rect(screen, (255, 0, 0), pygame.rect.Rect(float(screen_width/2), 100.0, 350.0, 150.0))
	square2 = pygame.draw.rect(screen, (255, 0, 0), pygame.rect.Rect(float(screen_width/2), 500.0, 350.0, 150.0))
	uj_jatek_szoveg = font_size50.render("New game", 0, BLACK)
	uj_jatek_szoveg_helye = (square1.left+5, square1.top+10)
	screen.blit(uj_jatek_szoveg, uj_jatek_szoveg_helye)
	pygame.display.update()