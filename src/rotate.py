import object_manager
import pygame
import math
from math import sin, cos, radians


def get_point_around_circle(center, radius, angle):
    x = -center[0] - radius * math.cos(math.radians(angle)) # minus is convert to pygame's coordinate system (-y is up)
    y = center[1] - radius * math.sin(math.radians(angle))
    return (x, y) 

def get_angle_from_decimal(angle):
    return int(angle * 360) % 360
    
def get_rotated_point(local_image_x, local_image_y, theta):
    x1 = round(cos(radians(theta)) * local_image_x - sin(radians(theta)) * local_image_y) # round is to avoid -15.99999999999999999996 (want -16)
    y1 = -round(sin(radians(theta)) * local_image_x + cos(radians(theta)) * local_image_y)
    return (x1, y1)

def move_rect_by_point(point_on_rect, new_point):
    diff_x = new_point[0] - point_on_rect[0]
    diff_y = new_point[1] - point_on_rect[1]

    return (diff_x, diff_y)



def main():
    running = True
    screen = pygame.display.set_mode((800, 600))
    pygame.display.set_caption("Translate")

    il = object_manager.BasicLoader()
    axe_texture = il.load("assets/wooden_axe.png")
    axe_texture = pygame.transform.scale(axe_texture, (96, 96))
    axe_texture = pygame.transform.rotate(axe_texture, 45) # make the axe texture vertical upright

    axe_end_pos = (400, 300)
    axe_angle = 0

    axe_rect = axe_texture.get_rect()
    axe_rect.midbottom = axe_end_pos

    axe_bottom_point = (axe_texture.get_width() / 2, axe_texture.get_height())

    steps = 60
    step_no = 0


    clock = pygame.time.Clock()

    print(get_point_around_circle((0, 0), 100, 0), get_point_around_circle((0, 0), 100, 0) == (0, -100))

    axe_rotator = Rotator(axe_rect.center, axe_rect.midbottom)


    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        screen.fill((0, 0, 0))

        angle = (-1 * get_angle_from_decimal(1 / steps * step_no))

        # draw the axe
        current_axe_texture = pygame.transform.rotate(axe_texture, angle)
        new_axe_center = axe_rotator(angle, axe_end_pos)
        axe_rect = current_axe_texture.get_rect(center=new_axe_center)
        tight_axe_surface = pygame.Surface((axe_texture.get_width(), axe_texture.get_height()))
        tight_axe_surface.blit(current_axe_texture, (0, 0))
        tight_axe_rect = tight_axe_surface.get_rect(center=new_axe_center)

        '''
        #print("axe_rect.pos: (" + str(axe_rect.x) + ", " + str(axe_rect.y) + ")\nend_point: (" + str(rp[0] + ))

        axe_rect.x = axe_end_pos[0]
        axe_rect.y = axe_end_pos[1]
        axe_rect.move(*rp)
        

        #axe_rect.y = axe_end_pos[1] - rp[1]

        if step_no % steps == 0:
            print("axe_rect.center:", axe_rect.center, "axe_end_pos:", axe_end_pos, "is_equal:", axe_rect.center == axe_end_pos)
        #axe_rect.midbottom = axe_end_pos
        '''


        screen.blit(current_axe_texture, axe_rect)
        pygame.draw.rect(screen, (0, 255, 0), tight_axe_rect, width=3) # axe bounding box

        screen.blit(axe_texture, (0, 0))


        pygame.display.update()

        step_no += 1

        clock.tick(steps)

class Rotator:
    def __init__(self, center, rotation_point, image_angle=0):
        x_mag = center[0] - rotation_point[0]
        y_mag = center[1] - rotation_point[1]
        self.radius = math.hypot(x_mag, y_mag)
        self.start_angle = math.atan2(-y_mag, x_mag) - math.radians(image_angle)

    def __call__(self, angle, rotation_point):
        new_angle = math.radians(angle) + self.start_angle
        new_x = rotation_point[0] + self.radius * math.cos(new_angle)
        new_y = rotation_point[1] - self.radius * math.sin(new_angle)
        return (new_x, new_y)

if __name__ == '__main__':
    main()
