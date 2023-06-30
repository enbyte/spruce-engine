import src as spruce
import pygame
from pygame.locals import * 

import player

pygame.init()
spruce.init()


flags = DOUBLEBUF | NOFRAME | SCALED | FULLSCREEN
screen = pygame.display.set_mode((1024, 640), flags=flags, vsync=1)

p = player.HaloBall('./light.png', 50, pygame.Color('cornflowerblue'))
pygame.mouse.set_visible(False)

running = True  

clock = pygame.time.Clock()


while running:
    for event in pygame.event.get():    
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == K_q:
                pygame.quit()
    
    screen.fill((0, 0, 0))
    p.update(pygame.mouse.get_pos())
    p.draw(screen)
    pygame.display.update()
    clock.tick(60)