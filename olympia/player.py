import pygame
pygame.init()

class HaloBall(pygame.sprite.Sprite):
    def __init__(self, image, radius, color):
        super().__init__()
        self.image = pygame.image.load(image).convert_alpha()
        self.image.set_colorkey((0, 0, 0))
        self.image = pygame.transform.scale(self.image, (radius, radius))
        if not pygame.Color(color) == pygame.Color('white'):
            pxbuf = pygame.PixelArray(self.image)
            completed_colors = {}
            for p in range(len(pxbuf)):
                row = pxbuf[p]
                for i in range(len(row)):
                    item = row[i]
                    if hex(item) == '0xff000000':
                        continue
                    z = str(hex(item))[4:]
                    if z in completed_colors:
                        pxbuf[p, i] = completed_colors[z]
                        continue
                    r = int(z[:2], 16)/255
                    print(z)
                    pxbuf[p, i] = (int(color.r * r), int(color.g * r), int(color.b * r))
                    completed_colors[z] = (int(color.r * r), int(color.g * r), int(color.b * r))

            del pxbuf

                
        self.rect = self.image.get_rect()
        self.radius = radius
        self.color = color
        self.rect.center = (0, 0)
        self.vel = [0, 0]

    def add_x_vel(self, speed):
        self.vel[0] += speed
    
    def add_y_vel(self, speed):
        self.vel[1] += speed

    def add_xy_vel(self, speedx, speedy):
        self.vel[0] += speedx
        self.vel[1] += speedy

    def goto_x(self, x):
        self.rect.x = x

    def goto_y(self, y):
        self.rect.y = y
    
    def goto_xy(self, x, y):
        self.rect.x = x
        self.rect.y = y

    def update(self, mousepos=None):
        if not mousepos is None:
            self.rect.center = mousepos
        self.rect.x += self.vel[0]
        self.rect.y += self.vel[1]
        self.vel = [0, 0]

    def draw(self, surface):
        surface.blit(self.image, self.rect, special_flags=pygame.BLEND_RGBA_ADD)

    
        