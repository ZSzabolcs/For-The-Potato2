import pygame

pygame.init()

window_width = 1000
window_height = 1000
window = pygame.display.set_mode((window_width, window_height))

background_image = pygame.image.load("")


run = 1
while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
