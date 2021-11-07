import pygame
import sys

file = sys.argv[1]
pygame.init()

img = pygame.image.load(file)

display = pygame.display.set_mode(img.get_size(), pygame.SCALED)
rect_surf = pygame.Surface((0, 0))
coords = [0, 0]

running = True
mousedown = False

while running:
    display.blit(img, (0, 0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mousedown = True
            coords = pygame.mouse.get_pos()
        elif event.type == pygame.MOUSEBUTTONUP:
            print("[%s, %s, %s, %s]" % (coords[0], coords[1], rect_surf.get_width(), rect_surf.get_height()))
            rect_surf = pygame.Surface((0, 0))
            mousedown = False
        elif event.type == pygame.MOUSEMOTION:
            if mousedown:
                rect_surf = pygame.Surface((abs(coords[0] - pygame.mouse.get_pos()[0]), abs(coords[1] - pygame.mouse.get_pos()[1])))
                rect_surf.fill((255, 255, 255))


    display.blit(rect_surf, (min(coords[0], pygame.mouse.get_pos()[0]), min(coords[1], pygame.mouse.get_pos()[1]))) 
    pygame.display.update()