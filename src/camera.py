import pygame

class Camera:
    def __init__(self, width, height, x, y):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.rect = pygame.Rect(x, y, width, height)
        self.surf = pygame.Surface((width, height))

    def draw_image(self, image, worldspace_x, worldspace_y):
        converted_x = worldspace_x - self.x
        converted_y = worldspace_y - self.y
        self.surf.blit(image, (converted_x, converted_y))

    def fill(self, color):
        self.surf.fill(color)

    def draw_to_display(self, display, offset_x=0, offset_y=0):
        display.blit(self.surf, (offset_x, offset_y))

    def goto(self, x, y):
        self.x = x
        self.y = y
        self.rect.x = x
        self.rect.y = y

    def move(self, x, y):
        self.x += x
        self.y += y
        self.rect.x += x
        self.rect.y += y